// main.go
// version 0.1.1

package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"os/exec"
	"time"
)
var AppVersion = "0.1.1"
var serverInstance *http.Server

func main() {
	host := flag.String("host", "127.0.0.1", "Server host to listen on")
	port := flag.String("port", "8080", "Server port to listen on")
	flag.Parse()

	mux := http.NewServeMux()
	mux.HandleFunc("/get_pot", HandleGetPot)

	// 1. Version Endpoint
	mux.HandleFunc("/version", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"name": "ytdlp-pot-provider", "version": "0.1.1"}`))
	})

	// 2. Health Check Endpoint (လွယ်ကူစွာ server အခြေအနေ စစ်ဆေးရန်)
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status": "healthy"}`))
	})

	// 3. Status Endpoint (Server ရဲ့ အသေးစိတ် အချက်အလက်များ)
	mux.HandleFunc("/status", HandleStatus)

	// 4. Shutdown Endpoint (Localhost ကနေပဲ ခွင့်ပြုရန်)
	mux.HandleFunc("/shutdown", func(w http.ResponseWriter, r *http.Request) {
		if !isLocalRequest(r) {
			http.Error(w, "Forbidden", http.StatusForbidden)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status": "shutting down..."}`))
		log.Println("Shutdown request received. Stopping server...")

		go func() {
			time.Sleep(500 * time.Millisecond)
			if serverInstance != nil {
				ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
				defer cancel()
				serverInstance.Shutdown(ctx)
			}
		}()
	})

	// 5. Restart Endpoint (Localhost ကနေပဲ ခွင့်ပြုရန်)
	mux.HandleFunc("/restart", func(w http.ResponseWriter, r *http.Request) {
		if !isLocalRequest(r) {
			http.Error(w, "Forbidden", http.StatusForbidden)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status": "restarting..."}`))
		log.Println("Restart request received. Restarting server...")

		go func() {
			time.Sleep(500 * time.Millisecond)

			// အသစ်ထွက်လာမည့် process ၏ log များကို လက်ရှိ terminal တွင် ပြန်ပေါ်စေရန်
			cmd := exec.Command(os.Args[0], os.Args[1:]...)
			cmd.Stdout = os.Stdout
			cmd.Stderr = os.Stderr
			_ = cmd.Start()

			if serverInstance != nil {
				ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
				defer cancel()
				serverInstance.Shutdown(ctx)
			}
		}()
	})

	// 3.5. Clear Cache Endpoint
	mux.HandleFunc("/clear_cache", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost && r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		log.Println("Received request to clear cache.")

		// TODO: သင်၏ Cache သိုလှောင်ရာ နေရာများကို ဤနေရာတွင် ရှင်းလင်းပါ (ဥပမာ- map, local cache files စသည်ဖြင့်)
		
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status": "success", "message": "Cache cleared successfully"}`))
	})

	addr := fmt.Sprintf("%s:%s", *host, *port)
	serverInstance = &http.Server{
		Addr:    addr,
		Handler: mux,
	}

	log.Printf("YawStar POT Server started and listening at http://%s", addr)
	if err := serverInstance.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Server failed: %v", err)
	} else {
		log.Println("Server stopped gracefully.")
	}
}

// Localhost ကလာသော Request ဟုတ်မဟုတ် စစ်ဆေးသည့် Helper function
func isLocalRequest(r *http.Request) bool {
	ip, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return false
	}
	return ip == "127.0.0.1" || ip == "::1" || ip == "localhost"
}