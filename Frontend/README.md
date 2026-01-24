# RAG Chatbot Professional - Frontend Documentation

This project is a professional-grade Electron-based frontend for a RAG (Retrieval-Augmented Generation) Chatbot. It features a ChatGPT-style UI with document management, chat history, speech-to-text queries, and real-time streaming simulations.

## ✨ Key Features
- **Multi-Modal Uploads**: Support for Documents, Videos, Audio, and Images.
- **Speech Queries**: Record voice prompts directly in the UI (MP3 format).
- **ChatGPT UI**: Modern, responsive layout with staged document previews.
- **Real-time Streaming**: Simulated token-by-token response generation.

## 🏗 Project Architecture

The application follows the Electron standard architecture, separating the **Main Process** (System/Node.js) from the **Renderer Process** (UI).

- **Main Process (`Frontend/src/index.js`)**: Handles window management, OS-level file dialogs, and simulated data storage.
- **Preload Script (`Frontend/src/preload.js`)**: A secure bridge that exposes specific Electron APIs to the frontend via `window.electronAPI`.
- **Renderer Process (`Frontend/src/renderer.js`)**: Manages the UI state, DOM updates, and user interactions.
- **Service Layer (`Frontend/src/services/ragService.js`)**: Contains the core logic for chatting and uploading. **This is the primary integration point for the backend.**

---

## 📂 File-by-File Explanation

### 1. `Frontend/src/index.js` (Main Process)
- **IPC Handlers**: Listens for requests from the frontend (e.g., `chat:send`, `chat:send-speech`, `documents:upload`).
- **Speech Support**: Receives raw MP3 buffers from the renderer and passes them to the service layer.
- **File Dialogs**: Uses Electron's `dialog.showOpenDialog` to allow users to select multiple documents, videos, audio, or images from their local system.

### 2. `Frontend/src/services/ragService.js` (RAG Logic)
This file simulates the RAG pipeline. To integrate a real backend, replace these methods with `fetch` or `axios` calls to your API.
- **`getResponse(message)`**: 
    - *Current*: Simulates a 1.5s delay, returns a mock markdown response, and randomly picks "sources".
    - *Integration*: Should POST the user message to your backend and return the LLM response + source metadata.
- **`processSpeechQuery(audioBuffer, fileName)`**:
    - *Current*: Receives a Node.js Buffer containing MP3 data, simulates transcription delay, and returns a mock response.
    - *Integration*: Should upload the MP3 buffer to your STT service (e.g., OpenAI Whisper), transcribe it, and then run the standard RAG flow on the text.
- **`uploadDocuments(filePaths, type)`**:
    - *Current*: Simulates a 2s delay and returns a success message.
    - *Integration*: Should send the file paths (or upload the files themselves) to your backend for chunking, embedding, and storage in a Vector DB.

### 3. `Frontend/src/renderer.js` (UI Logic)
- **State Management**:
    - `currentSession`: Tracks the active chat messages and session metadata.
    - `uploadedDocs`: A temporary "staging" area for files uploaded or **recorded audio** (MP3) before sending.
- **Key Functions**:
    - `toggleRecording()`: Uses the MediaRecorder API to capture audio, converts it to an MP3-compatible blob, and stages it for sending.
    - `renderUploadedDocs()`: Dynamically updates the preview area with document icons or a microphone icon for audio queries.
    - `handleSendMessage()`: Orchestrates sending text or **speech queries**, triggering the "streaming" bot response.

### 4. `Frontend/src/index.html` & `index.css`
- **Mic Icon**: A new interactive mic button with a pulsing recording animation.
- **Input Area**: Optimized for multi-document previews with a auto-expanding textarea.

---

## 🚀 Integration Guide for Backend/Vector DB Developers

### 1. Document Indexing Flow
1. User selects files via the "Upload" button.
2. `index.js` captures absolute paths.
3. `ragService.uploadDocuments` receives these paths.
4. **Action**: Implement an endpoint that takes these paths (or file streams), generates embeddings, and inserts them into your Vector DB (e.g., Pinecone, Chroma, Milvus).

### 2. Speech/Audio Query Flow
1. User clicks the Mic icon and records their query.
2. `renderer.js` captures the audio and converts it to a `Uint8Array` (MP3 Buffer).
3. `index.js` passes the buffer to `ragService.processSpeechQuery`.
4. **Action**: Implement an **STT-to-RAG** flow:
    - Transcribe the MP3 buffer using a model like **Whisper**.
    - Use the resulting text to perform a similarity search in your Vector DB.
    - Generate an LLM response based on the retrieved context.

### 3. Chat/Retrieval Flow
1. User sends a message.
2. `renderer.js` calls `ragService.getResponse`.
3. **Action**: Implement a RAG endpoint that returns text and source metadata.

### 4. Expected Data Formats
- **Speech Query Request**:
  - `audioBuffer`: Node.js `Buffer` (MP3 encoded).
  - `fileName`: String (e.g., `speech_query_1706123456.mp3`).
- **Message Response**:
  ```json
  {
    "text": "The response string (Markdown supported)",
    "sources": ["file1.pdf", "file2.docx"]
  }
  ```
- **Upload Response**:
  ```json
  {
    "success": true,
    "message": "Files indexed successfully",
    "uploadedFiles": [{ "name": "file.pdf", "type": "document" }]
  }
  ```

---

## 🛠 Setup & Development

1. **Install Dependencies**:
   ```bash
   cd Frontend
   npm install
   ```
2. **Start Application**:
   ```bash
   npm start
   ```
3. **Distribution**:
   ```bash
   npm run make
   ```

---
*Note: The current implementation uses a `mockStorage` in `index.js`. For a production app, replace this with a local SQLite database or a persistent cloud backend.*
