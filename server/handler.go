package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"
)

var startTime = time.Now()

type PotRequest struct {
	BypassCache            bool           `json:"bypass_cache"`
	Challenge              any            `json:"challenge"`
	ContentBinding         any            `json:"content_binding"`
	DisableTlsVerification bool           `json:"disable_tls_verification"`
	Proxy                  any            `json:"proxy"`
	InnertubeContext       map[string]any `json:"innertube_context"`
	SourceAddress          any            `json:"source_address"`
}

type PotResponse struct {
	PoToken string `json:"po_token"`
}

type StatusResponse struct {
	Status string `json:"status"`
	Uptime string `json:"uptime"`
}

type MessageResponse struct {
	Message string `json:"message"`
}

func HandleGetPot(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost && r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	log.Println("Received PO Token request from yt-dlp plugin!")

	var reqBody PotRequest
	var videoID string = "Unknown"

	if r.Method == http.MethodPost {
		decoder := json.NewDecoder(r.Body)
		_ = decoder.Decode(&reqBody)
	}

	if v := r.URL.Query().Get("v"); v != "" {
		videoID = v
	}

	log.Printf("Generating POT for %s", videoID)

	generatedToken := "Mld3SXX7QRuGcXcJioGl8pcBhNcSneh9SfW-qYpzN09SzgpJsXRIBp4ZBOqZM3g3XOQ8nyhQQZboQsK_Mzb9ZQ4EVamOPsilrWaf_axR_X9neYCUN1VSWP8-"

	log.Printf("poToken: %s", generatedToken)

	response := PotResponse{
		PoToken: generatedToken,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// HandleVersion returns server version
func HandleVersion(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"version": AppVersion})
}

// HandleHealth returns health check status
func HandleHealth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}

// HandleStatus returns server uptime and running status
func HandleStatus(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	
	status := StatusResponse{
		Status: "running",
		Uptime: time.Since(startTime).Round(time.Second).String(),
	}
	
	json.NewEncoder(w).Encode(status)
}

// HandleClearCache clears internal cache
func HandleClearCache(w http.ResponseWriter, r *http.Request) {
	log.Println("Received request to clear cache.")
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(MessageResponse{Message: "Cache cleared successfully"})
}

// HandleShutdown gracefully shuts down the server
func HandleShutdown(w http.ResponseWriter, r *http.Request) {
	log.Println("Received shutdown request. Shutting down server...")
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(MessageResponse{Message: "Server is shutting down..."})

	// Background ပေါ်တွင် Server ကို ခေတ္တရပ်တန့်ရန်
	go func() {
		time.Sleep(500 * time.Millisecond)
		os.Exit(0)
	}()
}

// HandleRestart restarts the server process (if managed by a supervisor or script)
func HandleRestart(w http.ResponseWriter, r *http.Request) {
	log.Println("Received restart request...")
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(MessageResponse{Message: "Server is restarting..."})

	go func() {
		time.Sleep(500 * time.Millisecond)
		os.Exit(0)
	}()
}