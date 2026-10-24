import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QHBoxLayout, QLabel)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile

class CloudMirrorClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cloud Mirroring PC Client")
        self.resize(1100, 700)

        # Theme Styling (Dark Mode)
        self.setStyleSheet("""
            QMainWindow { background-color: #11111b; }
            QWidget { font-family: 'Segoe UI', sans-serif; }
            QLineEdit { padding: 10px; border-radius: 6px; border: 1px solid #45475a; background-color: #1e1e2e; color: #cdd6f4; font-size: 14px; }
            QPushButton { padding: 10px 20px; border-radius: 6px; background-color: #89b4fa; color: #11111b; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background-color: #b4befe; }
            QLabel { color: #cdd6f4; font-size: 14px; font-weight: bold; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Bar Kontrol Bagian Atas
        top_bar = QHBoxLayout()
        self.label = QLabel("ID Stream Android:")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Paste ID dari HP di sini...")
        
        self.connect_btn = QPushButton("Hubungkan")
        self.connect_btn.clicked.connect(self.connect_to_stream)

        top_bar.addWidget(self.label)
        top_bar.addWidget(self.id_input)
        top_bar.addWidget(self.connect_btn)
        layout.addLayout(top_bar)

        # Web Engine View (Browser untuk me-render video & audio WebRTC)
        self.web_view = QWebEngineView()
        
        # Konfigurasi Kebijakan Autoplay Audio
        # Penting: Mengizinkan audio langsung berbunyi tanpa perlu interaksi klik dari user
        profile = QWebEngineProfile.defaultProfile()
        profile.settings().setAttribute(profile.settings().WebAttribute.PlaybackRequiresUserGesture, False)
        
        layout.addWidget(self.web_view)

    def connect_to_stream(self):
        peer_id = self.id_input.text().strip()
        if not peer_id:
            return

        # Template HTML Receiver yang diinjeksi langsung ke WebEngine View
        receiver_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
            <style>
                body {{ margin: 0; background-color: #000; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }}
                video {{ width: 100%; height: 100%; object-fit: contain; }}
            </style>
        </head>
        <body>
            <video id="remoteVideo" autoplay playsinline></video>
            <script>
                const peer = new Peer();
                peer.on('open', () => {{
                    // Panggil HP Android menggunakan ID yang dimasukkan
                    const call = peer.call('{peer_id}', new MediaStream());
                    
                    // Ketika HP mengirimkan stream video/audio
                    call.on('stream', remoteStream => {{
                        const video = document.getElementById('remoteVideo');
                        video.srcObject = remoteStream;
                        video.play();
                    }});
                }});
            </script>
        </body>
        </html>
        """
        # Muat kode HTML secara in-memory
        self.web_view.setHtml(receiver_html)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CloudMirrorClient()
    window.show()
    sys.exit(app.exec())
