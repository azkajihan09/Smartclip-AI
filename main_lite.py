#!/usr/bin/env python3
"""
Smartclip AI - Main Application (Lite Version for Testing)
Version tanpa dependencies AI yang berat untuk testing GUI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import threading
import os
import sys
from pathlib import Path
import queue
import time
from datetime import datetime

# Setup CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SmartclipAILite:
    def __init__(self):
        print("Initializing Smartclip AI Lite...")
        
        # Setup main window
        self.root = ctk.CTk()
        self.root.title("Smartclip AI - YouTube Video Processor (Lite)")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Initialize processing queue dan status
        self.processing_queue = queue.Queue()
        self.is_processing = False
        self.current_progress = 0
        
        # Setup directories
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.temp_dir = self.base_dir / "temp"
        
        # Ensure directories exist
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        
        print("Setting up UI...")
        self.setup_ui()
        print("Smartclip AI Lite initialized successfully!")
        
    def setup_ui(self):
        """Setup user interface"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.setup_header()
        
        # Input Section
        self.setup_input_section()
        
        # Processing Options
        self.setup_processing_options()
        
        # Progress Section
        self.setup_progress_section()
        
        # Control Buttons
        self.setup_control_buttons()
        
        # Status Bar
        self.setup_status_bar()
        
    def setup_header(self):
        """Setup header section"""
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🎬 Smartclip AI (Lite Version)", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        subtitle_label = ctk.CTkLabel(
            header_frame, 
            text="Testing version - AI features will be available after installing dependencies",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        )
        subtitle_label.pack(pady=(0, 20))
        
    def setup_input_section(self):
        """Setup input section untuk URL YouTube"""
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        input_title = ctk.CTkLabel(
            input_frame, 
            text="📹 Input Video", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        input_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # URL Input
        url_frame = ctk.CTkFrame(input_frame)
        url_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        url_label = ctk.CTkLabel(url_frame, text="URL YouTube:")
        url_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.url_entry = ctk.CTkEntry(
            url_frame, 
            placeholder_text="Masukkan URL YouTube (contoh: https://www.youtube.com/watch?v=...)",
            height=40
        )
        self.url_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # File input alternative
        file_frame = ctk.CTkFrame(input_frame)
        file_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        file_label = ctk.CTkLabel(file_frame, text="Atau pilih file video lokal:")
        file_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        file_button_frame = ctk.CTkFrame(file_frame)
        file_button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ctk.CTkEntry(
            file_button_frame, 
            textvariable=self.file_path_var,
            placeholder_text="Path file video...",
            state="readonly"
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(
            file_button_frame,
            text="Browse",
            command=self.browse_video_file,
            width=100
        )
        browse_button.pack(side="right")
        
    def setup_processing_options(self):
        """Setup opsi pemrosesan"""
        options_frame = ctk.CTkFrame(self.main_frame)
        options_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        options_title = ctk.CTkLabel(
            options_frame, 
            text="⚙️ Opsi Pemrosesan AI", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        options_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Two column layout
        columns_frame = ctk.CTkFrame(options_frame)
        columns_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Left column
        left_column = ctk.CTkFrame(columns_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # AI Analysis Options
        self.detect_moments = tk.BooleanVar(value=True)
        moments_cb = ctk.CTkCheckBox(left_column, text="🎯 Auto-detect moment terbaik", variable=self.detect_moments)
        moments_cb.pack(anchor="w", padx=10, pady=5)
        
        self.face_tracking = tk.BooleanVar(value=True)
        face_cb = ctk.CTkCheckBox(left_column, text="👤 Smart face tracking", variable=self.face_tracking)
        face_cb.pack(anchor="w", padx=10, pady=5)
        
        self.speaker_detection = tk.BooleanVar(value=True)
        speaker_cb = ctk.CTkCheckBox(left_column, text="🎙️ Deteksi pembicara", variable=self.speaker_detection)
        speaker_cb.pack(anchor="w", padx=10, pady=5)
        
        # Right column
        right_column = ctk.CTkFrame(columns_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.auto_subtitle = tk.BooleanVar(value=True)
        subtitle_cb = ctk.CTkCheckBox(right_column, text="📝 Auto subtitle", variable=self.auto_subtitle)
        subtitle_cb.pack(anchor="w", padx=10, pady=5)
        
        self.add_watermark = tk.BooleanVar(value=False)
        watermark_cb = ctk.CTkCheckBox(right_column, text="🔖 Tambah watermark", variable=self.add_watermark)
        watermark_cb.pack(anchor="w", padx=10, pady=5)
        
        self.podcast_mode = tk.BooleanVar(value=False)
        podcast_cb = ctk.CTkCheckBox(right_column, text="🎙️ Mode podcast (split)", variable=self.podcast_mode)
        podcast_cb.pack(anchor="w", padx=10, pady=5)
        
    def setup_progress_section(self):
        """Setup progress tracking section"""
        progress_frame = ctk.CTkFrame(self.main_frame)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        progress_title = ctk.CTkLabel(
            progress_frame, 
            text="📊 Progress Pemrosesan", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        progress_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            variable=self.progress_var,
            height=20
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        
        # Progress text
        self.progress_text = ctk.CTkLabel(
            progress_frame,
            text="Siap untuk memproses...",
            font=ctk.CTkFont(size=12)
        )
        self.progress_text.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Status info
        self.status_info = ctk.CTkLabel(
            progress_frame,
            text="Status: GUI loaded successfully. Ready for input.",
            font=ctk.CTkFont(size=10),
            text_color="gray70"
        )
        self.status_info.pack(anchor="w", padx=20, pady=(0, 20))
        
    def setup_control_buttons(self):
        """Setup control buttons"""
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(fill="x", pady=(0, 20))
        
        # Button container
        button_container = ctk.CTkFrame(button_frame)
        button_container.pack(expand=True, pady=20)
        
        # Start processing button - Main action
        self.start_button = ctk.CTkButton(
            button_container,
            text="🚀 Mulai Proses",
            command=self.start_processing,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=200,
            fg_color="#1f538d"
        )
        self.start_button.pack(side="left", padx=10)
        
        # Install AI button
        self.install_button = ctk.CTkButton(
            button_container,
            text="🤖 Install AI Features",
            command=self.show_install_info,
            font=ctk.CTkFont(size=14),
            height=50,
            width=180,
            fg_color="#2d5530"
        )
        self.install_button.pack(side="left", padx=10)
        
        # Test GUI button  
        self.test_button = ctk.CTkButton(
            button_container,
            text="🧪 Test",
            command=self.test_gui,
            font=ctk.CTkFont(size=14),
            height=50,
            width=120,
            fg_color="#6b5b73"
        )
        self.test_button.pack(side="left", padx=10)
        
    def setup_status_bar(self):
        """Setup status bar"""
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.pack(fill="x", side="bottom")
        
        self.status_text = ctk.CTkLabel(
            status_frame,
            text="✅ GUI ready - This is lite version for testing interface",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_text.pack(fill="x", padx=20, pady=10)
        
    def browse_video_file(self):
        """Browse untuk memilih file video lokal"""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.webm *.m4v"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Pilih File Video",
            filetypes=filetypes
        )
        
        if filename:
            self.file_path_var.set(filename)
            self.url_entry.delete(0, 'end')  # Clear URL if file is selected
            self.update_status(f"File terpilih: {Path(filename).name}")
            
    def start_processing(self):
        """Start video processing dengan simulasi"""
        # Validate input
        youtube_url = self.url_entry.get().strip()
        file_path = self.file_path_var.get().strip()
        
        if not youtube_url and not file_path:
            messagebox.showerror("Input Required", "Masukkan URL YouTube atau pilih file video!")
            return
            
        # Check selected options
        selected_options = []
        if self.detect_moments.get():
            selected_options.append("Auto-detect moment terbaik")
        if self.face_tracking.get():
            selected_options.append("Face tracking")
        if self.speaker_detection.get():
            selected_options.append("Deteksi pembicara")
        if self.auto_subtitle.get():
            selected_options.append("Auto subtitle")
        if self.add_watermark.get():
            selected_options.append("Watermark")
        if self.podcast_mode.get():
            selected_options.append("Mode podcast")
            
        if not selected_options:
            messagebox.showwarning("No Options", "Pilih minimal satu opsi pemrosesan!")
            return
        
        # Show processing simulation
        self.simulate_processing(youtube_url or file_path, selected_options)
        
    def simulate_processing(self, input_source, options):
        """Simulate video processing workflow"""
        self.update_status("🚀 Memulai pemrosesan...")
        
        # Disable buttons during processing
        self.start_button.configure(state="disabled")
        self.install_button.configure(state="disabled")
        
        steps = [
            "📥 Download video dari YouTube...",
            "🎯 Analisis video untuk moment terbaik...",
            "👤 Deteksi dan tracking wajah...",
            "🎙️ Analisis suara dan identifikasi pembicara...", 
            "📝 Generate subtitle otomatis...",
            "🔖 Menambahkan watermark...",
            "✂️ Memotong dan editing video...",
            "💾 Menyimpan hasil akhir..."
        ]
        
        # Simulate processing steps
        threading.Thread(target=self._process_simulation, args=(steps, options), daemon=True).start()
        
    def _process_simulation(self, steps, options):
        """Background processing simulation"""
        total_steps = len(steps)
        
        for i, step in enumerate(steps):
            # Update progress
            progress = (i / total_steps) * 100
            self.root.after(0, lambda p=progress, s=step: self.update_progress(p, s))
            
            # Simulate processing time
            import random
            time.sleep(random.uniform(1.0, 3.0))
        
        # Completion
        self.root.after(0, self._processing_complete)
        
    def _processing_complete(self):
        """Handle processing completion"""
        self.update_progress(100, "✅ Pemrosesan selesai!")
        
        # Show results
        result_message = """🎉 Video berhasil diproses!

📁 Hasil disimpan di:
   • output/smartclip_result.mp4
   • output/subtitles.srt
   • output/analysis_report.txt

⏱️ Waktu proses: 2 menit 30 detik
📊 Moment terbaik: 5 clip ditemukan
👥 Speaker: 2 orang teridentifikasi

Note: Ini adalah simulasi. Install AI dependencies untuk pemrosesan sebenarnya."""

        messagebox.showinfo("Processing Complete", result_message)
        
        # Re-enable buttons
        self.start_button.configure(state="normal")
        self.install_button.configure(state="normal")
        
        self.update_status("✅ Siap untuk pemrosesan selanjutnya")
    def test_gui(self):
        """Test GUI functionality"""
        self.update_progress(0, "Testing GUI components...")
        
        # Test progress bar
        for i in range(101):
            self.update_progress(i, f"Testing progress: {i}%")
            time.sleep(0.01)  # Small delay to see progress
            
        self.update_status("✅ GUI test completed successfully!")
        messagebox.showinfo("Test Complete", "GUI is working properly!\n\nNext steps:\n1. Run install_ai.py to install AI dependencies\n2. Restart and use full version")
        
    def show_install_info(self):
        """Show installation information"""
        info_text = """🤖 Install AI Dependencies untuk fitur lengkap:

🚀 Quick Install:
   python install_ai.py

📦 Manual Install:
   pip install torch torchvision torchaudio
   pip install openai-whisper face-recognition
   pip install pyannote.audio librosa opencv-python

⚡ Fitur AI yang tersedia setelah install:
   • 🎯 Auto-detect moment terbaik dengan AI
   • 👤 Smart face tracking dan recognition
   • 🎙️ Speaker diarization (identifikasi pembicara)
   • 📝 Automatic speech-to-text subtitle
   • 🧠 Advanced video analysis dengan deep learning

💡 Tips:
   - Install memerlukan ~2-3GB download
   - Gunakan Wi-Fi untuk download dependencies
   - Restart aplikasi setelah install selesai"""
        
        messagebox.showinfo("AI Features Installation", info_text)
        
    def reset_form(self):
        """Reset form ke kondisi awal"""
        # Clear inputs
        self.url_entry.delete(0, 'end')
        self.file_path_var.set("")
        
        # Reset progress
        self.progress_var.set(0)
        self.progress_text.configure(text="Siap untuk memproses...")
        
        # Reset status
        self.update_status("✅ Form direset - GUI ready")
        
    def update_progress(self, percentage, message):
        """Update progress bar dan message"""
        self.progress_var.set(percentage / 100.0)
        self.progress_text.configure(text=message)
        self.root.update()  # Force GUI update
        
    def update_status(self, message):
        """Update status bar"""
        self.status_text.configure(text=message)
        
    def run(self):
        """Run the application"""
        print("Starting GUI...")
        self.root.mainloop()

def main():
    """Main function"""
    try:
        print("=" * 50)
        print("SMARTCLIP AI - LITE VERSION")
        print("=" * 50)
        print()
        print("This is the lite version for testing the GUI.")
        print("AI features require additional dependencies.")
        print()
        
        app = SmartclipAILite()
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        try:
            messagebox.showerror("Startup Error", f"Gagal memulai aplikasi: {str(e)}")
        except:
            print("Failed to show error dialog")

if __name__ == "__main__":
    main()