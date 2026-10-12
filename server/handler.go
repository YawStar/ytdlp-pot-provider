package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

var startTime = time.Now()

type PotResponse struct {
	PoToken string `json:"po_token"`
}

type StatusResponse struct {
	Status string `json:"status"`
	Uptime string `json:"uptime"`
}

func HandleGetPot(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost && r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	log.Println("Received PO Token request from yt-dlp plugin!")

	response := PotResponse{
		PoToken: "YOUR_GENERATED_PO_TOKEN_HERE",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
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