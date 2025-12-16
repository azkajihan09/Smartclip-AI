#!/usr/bin/env python3
"""
Smartclip AI - Aplikasi AI untuk analisis dan editing video YouTube secara otomatis
Fitur: Auto-detect moment terbaik, face tracking, speaker identification, 
       subtitle otomatis, watermark, dan podcast mode split
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

# Import modules lokal
sys.path.append(str(Path(__file__).parent))
from config import *
from modules.youtube_downloader import YouTubeDownloader
from modules.video_analyzer import VideoAnalyzer
from modules.face_tracker import FaceTracker
from modules.speaker_diarization import SpeakerDiarization
from modules.subtitle_generator import SubtitleGenerator
from modules.video_editor import VideoEditor
from modules.utils import Utils

class SmartclipAI:
    def __init__(self):
        # Setup main window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Smartclip AI - YouTube Video Processor")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Initialize processing queue dan status
        self.processing_queue = queue.Queue()
        self.is_processing = False
        self.current_progress = 0
        
        # Initialize modules
        self.youtube_dl = YouTubeDownloader()
        self.video_analyzer = VideoAnalyzer()
        self.face_tracker = FaceTracker()
        self.speaker_diarization = SpeakerDiarization()
        self.subtitle_generator = SubtitleGenerator()
        self.video_editor = VideoEditor()
        self.utils = Utils()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup user interface"""
        # Main container dengan scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.setup_header()
        
        # Input Section
        self.setup_input_section()
        
        # Processing Options
        self.setup_processing_options()
        
        # Output Settings
        self.setup_output_settings()
        
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
            text="🎬 Smartclip AI", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        subtitle_label = ctk.CTkLabel(
            header_frame, 
            text="Analisis Video YouTube dengan AI - Deteksi Moment Terbaik, Face Tracking, Auto Subtitle",
            font=ctk.CTkFont(size=14),
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
        
        self.auto_subtitle = tk.BooleanVar(value=True)
        subtitle_cb = ctk.CTkCheckBox(left_column, text="📝 Auto subtitle", variable=self.auto_subtitle)
        subtitle_cb.pack(anchor="w", padx=10, pady=5)
        
        # Right column
        right_column = ctk.CTkFrame(columns_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.add_watermark = tk.BooleanVar(value=False)
        watermark_cb = ctk.CTkCheckBox(right_column, text="🔖 Tambah watermark", variable=self.add_watermark)
        watermark_cb.pack(anchor="w", padx=10, pady=5)
        
        self.podcast_mode = tk.BooleanVar(value=False)
        podcast_cb = ctk.CTkCheckBox(right_column, text="🎙️ Mode podcast (split atas-bawah)", variable=self.podcast_mode)
        podcast_cb.pack(anchor="w", padx=10, pady=5)
        
        self.scene_analysis = tk.BooleanVar(value=True)
        scene_cb = ctk.CTkCheckBox(right_column, text="🎬 Analisis perubahan scene", variable=self.scene_analysis)
        scene_cb.pack(anchor="w", padx=10, pady=5)
        
        self.audio_enhancement = tk.BooleanVar(value=False)
        audio_cb = ctk.CTkCheckBox(right_column, text="🔊 Peningkatan kualitas audio", variable=self.audio_enhancement)
        audio_cb.pack(anchor="w", padx=10, pady=5)
        
    def setup_output_settings(self):
        """Setup pengaturan output"""
        output_frame = ctk.CTkFrame(self.main_frame)
        output_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        output_title = ctk.CTkLabel(
            output_frame, 
            text="📁 Pengaturan Output", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        output_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Output directory
        dir_frame = ctk.CTkFrame(output_frame)
        dir_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        dir_label = ctk.CTkLabel(dir_frame, text="Folder Output:")
        dir_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        dir_button_frame = ctk.CTkFrame(dir_frame)
        dir_button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.output_dir_var = tk.StringVar(value=str(OUTPUT_DIR))\n        self.output_dir_entry = ctk.CTkEntry(\n            dir_button_frame, \n            textvariable=self.output_dir_var,\n            state=\"readonly\"\n        )\n        self.output_dir_entry.pack(side=\"left\", fill=\"x\", expand=True, padx=(0, 10))\n        \n        output_browse_button = ctk.CTkButton(\n            dir_button_frame,\n            text=\"Browse\",\n            command=self.browse_output_dir,\n            width=100\n        )\n        output_browse_button.pack(side=\"right\")\n        \n        # Quality and format settings\n        quality_frame = ctk.CTkFrame(output_frame)\n        quality_frame.pack(fill=\"x\", padx=20, pady=(0, 20))\n        \n        # Left side - Quality\n        quality_left = ctk.CTkFrame(quality_frame)\n        quality_left.pack(side=\"left\", fill=\"both\", expand=True, padx=(0, 10))\n        \n        quality_label = ctk.CTkLabel(quality_left, text=\"Kualitas Video:\")\n        quality_label.pack(anchor=\"w\", padx=10, pady=(10, 5))\n        \n        self.quality_var = tk.StringVar(value=\"720p\")\n        quality_menu = ctk.CTkOptionMenu(\n            quality_left,\n            variable=self.quality_var,\n            values=[\"480p\", \"720p\", \"1080p\", \"1440p\", \"4K\"]\n        )\n        quality_menu.pack(fill=\"x\", padx=10, pady=(0, 10))\n        \n        # Right side - Format\n        format_right = ctk.CTkFrame(quality_frame)\n        format_right.pack(side=\"right\", fill=\"both\", expand=True, padx=(10, 0))\n        \n        format_label = ctk.CTkLabel(format_right, text=\"Format Output:\")\n        format_label.pack(anchor=\"w\", padx=10, pady=(10, 5))\n        \n        self.format_var = tk.StringVar(value=\"mp4\")\n        format_menu = ctk.CTkOptionMenu(\n            format_right,\n            variable=self.format_var,\n            values=[\"mp4\", \"avi\", \"mov\", \"mkv\"]\n        )\n        format_menu.pack(fill=\"x\", padx=10, pady=(0, 10))\n        \n    def setup_progress_section(self):\n        \"\"\"Setup progress tracking section\"\"\"\n        progress_frame = ctk.CTkFrame(self.main_frame)\n        progress_frame.pack(fill=\"x\", pady=(0, 20))\n        \n        # Title\n        progress_title = ctk.CTkLabel(\n            progress_frame, \n            text=\"📊 Progress Pemrosesan\", \n            font=ctk.CTkFont(size=18, weight=\"bold\")\n        )\n        progress_title.pack(anchor=\"w\", padx=20, pady=(20, 10))\n        \n        # Progress bar\n        self.progress_var = tk.DoubleVar()\n        self.progress_bar = ctk.CTkProgressBar(\n            progress_frame,\n            variable=self.progress_var,\n            height=20\n        )\n        self.progress_bar.pack(fill=\"x\", padx=20, pady=(0, 10))\n        \n        # Progress text\n        self.progress_text = ctk.CTkLabel(\n            progress_frame,\n            text=\"Siap untuk memproses...\",\n            font=ctk.CTkFont(size=12)\n        )\n        self.progress_text.pack(anchor=\"w\", padx=20, pady=(0, 10))\n        \n        # Estimated time\n        self.time_estimate = ctk.CTkLabel(\n            progress_frame,\n            text=\"Perkiraan waktu: -\",\n            font=ctk.CTkFont(size=11),\n            text_color=\"gray70\"\n        )\n        self.time_estimate.pack(anchor=\"w\", padx=20, pady=(0, 20))\n        \n    def setup_control_buttons(self):\n        \"\"\"Setup control buttons\"\"\"\n        button_frame = ctk.CTkFrame(self.main_frame)\n        button_frame.pack(fill=\"x\", pady=(0, 20))\n        \n        # Button container\n        button_container = ctk.CTkFrame(button_frame)\n        button_container.pack(expand=True, pady=20)\n        \n        # Start processing button\n        self.start_button = ctk.CTkButton(\n            button_container,\n            text=\"🚀 Mulai Proses AI\",\n            command=self.start_processing,\n            font=ctk.CTkFont(size=16, weight=\"bold\"),\n            height=50,\n            width=200\n        )\n        self.start_button.pack(side=\"left\", padx=10)\n        \n        # Stop button\n        self.stop_button = ctk.CTkButton(\n            button_container,\n            text=\"⏹️ Stop\",\n            command=self.stop_processing,\n            font=ctk.CTkFont(size=16),\n            height=50,\n            width=120,\n            state=\"disabled\"\n        )\n        self.stop_button.pack(side=\"left\", padx=10)\n        \n        # Reset button\n        self.reset_button = ctk.CTkButton(\n            button_container,\n            text=\"🔄 Reset\",\n            command=self.reset_form,\n            font=ctk.CTkFont(size=16),\n            height=50,\n            width=120\n        )\n        self.reset_button.pack(side=\"left\", padx=10)\n        \n    def setup_status_bar(self):\n        \"\"\"Setup status bar\"\"\"\n        status_frame = ctk.CTkFrame(self.main_frame)\n        status_frame.pack(fill=\"x\", side=\"bottom\")\n        \n        self.status_text = ctk.CTkLabel(\n            status_frame,\n            text=\"✅ Siap - Masukkan URL YouTube atau pilih file video lokal\",\n            font=ctk.CTkFont(size=11),\n            anchor=\"w\"\n        )\n        self.status_text.pack(fill=\"x\", padx=20, pady=10)\n        \n    def browse_video_file(self):\n        \"\"\"Browse untuk memilih file video lokal\"\"\"\n        filetypes = [\n            (\"Video files\", \"*.mp4 *.avi *.mov *.mkv *.webm *.m4v\"),\n            (\"All files\", \"*.*\")\n        ]\n        \n        filename = filedialog.askopenfilename(\n            title=\"Pilih File Video\",\n            filetypes=filetypes\n        )\n        \n        if filename:\n            self.file_path_var.set(filename)\n            self.url_entry.delete(0, 'end')  # Clear URL if file is selected\n            self.update_status(f\"File terpilih: {Path(filename).name}\")\n            \n    def browse_output_dir(self):\n        \"\"\"Browse untuk memilih folder output\"\"\"\n        directory = filedialog.askdirectory(\n            title=\"Pilih Folder Output\",\n            initialdir=self.output_dir_var.get()\n        )\n        \n        if directory:\n            self.output_dir_var.set(directory)\n            self.update_status(f\"Folder output: {directory}\")\n            \n    def start_processing(self):\n        \"\"\"Mulai proses AI\"\"\"\n        # Validate input\n        url = self.url_entry.get().strip()\n        file_path = self.file_path_var.get().strip()\n        \n        if not url and not file_path:\n            messagebox.showerror(\"Error\", \"Masukkan URL YouTube atau pilih file video!\")\n            return\n            \n        if url and file_path:\n            messagebox.showerror(\"Error\", \"Pilih salah satu: URL YouTube atau file lokal!\")\n            return\n            \n        # Disable controls\n        self.start_button.configure(state=\"disabled\")\n        self.stop_button.configure(state=\"normal\")\n        \n        # Start processing in thread\n        self.is_processing = True\n        processing_thread = threading.Thread(\n            target=self.process_video,\n            args=(url if url else file_path, url != \"\")\n        )\n        processing_thread.daemon = True\n        processing_thread.start()\n        \n    def stop_processing(self):\n        \"\"\"Stop proses AI\"\"\"\n        self.is_processing = False\n        self.start_button.configure(state=\"normal\")\n        self.stop_button.configure(state=\"disabled\")\n        self.update_status(\"❌ Proses dihentikan oleh pengguna\")\n        self.update_progress(0, \"Proses dibatalkan\")\n        \n    def reset_form(self):\n        \"\"\"Reset form ke kondisi awal\"\"\"\n        # Clear inputs\n        self.url_entry.delete(0, 'end')\n        self.file_path_var.set(\"\")\n        \n        # Reset progress\n        self.progress_var.set(0)\n        self.progress_text.configure(text=\"Siap untuk memproses...\")\n        self.time_estimate.configure(text=\"Perkiraan waktu: -\")\n        \n        # Reset status\n        self.update_status(\"✅ Form direset - Siap untuk input baru\")\n        \n        # Enable controls\n        self.start_button.configure(state=\"normal\")\n        self.stop_button.configure(state=\"disabled\")\n        \n    def process_video(self, input_source, is_url=True):\n        \"\"\"Main processing function\"\"\"\n        try:\n            start_time = time.time()\n            \n            # Step 1: Download or load video\n            if is_url:\n                self.update_progress(10, \"📥 Mengunduh video dari YouTube...\")\n                video_path = self.youtube_dl.download(input_source)\n            else:\n                self.update_progress(10, \"📂 Memuat file video...\")\n                video_path = input_source\n                \n            if not video_path or not self.is_processing:\n                return\n                \n            # Step 2: Analyze video for best moments\n            if self.detect_moments.get():\n                self.update_progress(25, \"🎯 Menganalisis moment terbaik dengan AI...\")\n                moments = self.video_analyzer.analyze_video(video_path)\n            else:\n                moments = None\n                \n            if not self.is_processing:\n                return\n                \n            # Step 3: Face tracking\n            face_data = None\n            if self.face_tracking.get():\n                self.update_progress(40, \"👤 Melakukan face tracking...\")\n                face_data = self.face_tracker.track_faces(video_path)\n                \n            if not self.is_processing:\n                return\n                \n            # Step 4: Speaker diarization\n            speaker_data = None\n            if self.speaker_detection.get():\n                self.update_progress(55, \"🎙️ Mengidentifikasi pembicara...\")\n                speaker_data = self.speaker_diarization.identify_speakers(video_path)\n                \n            if not self.is_processing:\n                return\n                \n            # Step 5: Generate subtitles\n            subtitle_data = None\n            if self.auto_subtitle.get():\n                self.update_progress(70, \"📝 Menggenerate subtitle otomatis...\")\n                subtitle_data = self.subtitle_generator.generate_subtitles(video_path)\n                \n            if not self.is_processing:\n                return\n                \n            # Step 6: Video editing and output\n            self.update_progress(85, \"🎬 Mengedit dan memproses video final...\")\n            \n            output_options = {\n                'moments': moments,\n                'face_data': face_data,\n                'speaker_data': speaker_data,\n                'subtitle_data': subtitle_data,\n                'add_watermark': self.add_watermark.get(),\n                'podcast_mode': self.podcast_mode.get(),\n                'quality': self.quality_var.get(),\n                'format': self.format_var.get(),\n                'output_dir': self.output_dir_var.get()\n            }\n            \n            output_files = self.video_editor.process_video(video_path, output_options)\n            \n            if not self.is_processing:\n                return\n                \n            # Step 7: Cleanup and finish\n            self.update_progress(100, \"✅ Proses selesai!\")\n            \n            end_time = time.time()\n            total_time = end_time - start_time\n            \n            # Show completion message\n            self.show_completion_dialog(output_files, total_time)\n            \n        except Exception as e:\n            if self.is_processing:\n                self.update_status(f\"❌ Error: {str(e)}\")\n                messagebox.showerror(\"Error\", f\"Terjadi kesalahan: {str(e)}\")\n        finally:\n            # Reset controls\n            if self.is_processing:\n                self.start_button.configure(state=\"normal\")\n                self.stop_button.configure(state=\"disabled\")\n                self.is_processing = False\n                \n    def update_progress(self, percentage, message):\n        \"\"\"Update progress bar dan message\"\"\"\n        self.root.after(0, lambda: self._update_progress_ui(percentage, message))\n        \n    def _update_progress_ui(self, percentage, message):\n        \"\"\"Update UI progress (run in main thread)\"\"\"\n        self.progress_var.set(percentage / 100.0)\n        self.progress_text.configure(text=message)\n        \n        # Update time estimate\n        if percentage > 0 and hasattr(self, 'process_start_time'):\n            elapsed = time.time() - self.process_start_time\n            estimated_total = elapsed / (percentage / 100.0)\n            remaining = estimated_total - elapsed\n            \n            if remaining > 0:\n                remaining_str = self.utils.format_duration(remaining)\n                self.time_estimate.configure(text=f\"Perkiraan waktu tersisa: {remaining_str}\")\n            else:\n                self.time_estimate.configure(text=\"Hampir selesai...\")\n        \n    def update_status(self, message):\n        \"\"\"Update status bar\"\"\"\n        self.root.after(0, lambda: self.status_text.configure(text=message))\n        \n    def show_completion_dialog(self, output_files, processing_time):\n        \"\"\"Show completion dialog\"\"\"\n        time_str = self.utils.format_duration(processing_time)\n        \n        message = f\"🎉 Proses selesai dalam {time_str}!\\n\\n\"\n        message += \"File output yang dihasilkan:\\n\"\n        \n        for file_path in output_files:\n            message += f\"• {Path(file_path).name}\\n\"\n            \n        message += f\"\\nLokasi: {self.output_dir_var.get()}\"\n        \n        result = messagebox.showinfo(\n            \"Proses Selesai\", \n            message\n        )\n        \n        # Ask if want to open output folder\n        if messagebox.askyesno(\"Buka Folder\", \"Ingin membuka folder output?\"):\n            self.utils.open_folder(self.output_dir_var.get())\n            \n    def run(self):\n        \"\"\"Run the application\"\"\"\n        # Set process start time\n        self.process_start_time = time.time()\n        \n        # Start main loop\n        self.root.mainloop()\n\ndef main():\n    \"\"\"Main function\"\"\"\n    try:\n        app = SmartclipAI()\n        app.run()\n    except Exception as e:\n        print(f\"Error starting application: {e}\")\n        messagebox.showerror(\"Startup Error\", f\"Gagal memulai aplikasi: {str(e)}\")\n\nif __name__ == \"__main__\":\n    main()