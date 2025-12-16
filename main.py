#!/usr/bin/env python3
"""
Smartclip AI - Smart Launcher
Otomatis memilih versi berdasarkan dependencies yang tersedia
"""

import sys
import importlib.util
import os
from pathlib import Path

def check_package(package_name):
    """Check apakah package tersedia"""
    try:
        spec = importlib.util.find_spec(package_name)
        return spec is not None
    except:
        return False

def print_startup_banner():
    """Print startup banner"""
    print("🎬" + "=" * 58 + "🎬")
    print("                    SMARTCLIP AI")
    print("        AI-Powered YouTube Video Processor")
    print("🎬" + "=" * 58 + "🎬")
    print()

def check_ai_dependencies():
    """Check AI dependencies availability"""
    print("🔍 Checking AI dependencies...")
    
    # Critical AI packages untuk full functionality
    critical_packages = [
        ('torch', 'PyTorch (Deep Learning)'),
        ('whisper', 'OpenAI Whisper (Speech Recognition)'),
        ('face_recognition', 'Face Recognition'),
        ('cv2', 'OpenCV (Computer Vision)')
    ]
try:
    from modules.youtube_downloader import YouTubeDownloader
    print("YouTubeDownloader imported")
    from modules.video_analyzer import VideoAnalyzer
    print("VideoAnalyzer imported") 
    from modules.face_tracker import FaceTracker
    print("FaceTracker imported")
    from modules.speaker_diarization import SpeakerDiarization
    print("SpeakerDiarization imported")
    from modules.subtitle_generator import SubtitleGenerator  
    print("SubtitleGenerator imported")
    from modules.video_editor import VideoEditor
    print("VideoEditor imported")
    from modules.utils import Utils
    print("Utils imported")
except ImportError as e:
    print(f"Error importing modules: {e}")
    messagebox.showerror("Import Error", f"Failed to import required modules: {e}")
    sys.exit(1)

class SmartclipAI:
    def __init__(self):
        print("Initializing SmartclipAI...")
        
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
        
        # Initialize modules dengan error handling
        print("Initializing modules...")
        try:
            self.youtube_dl = YouTubeDownloader()
            print("✓ YouTubeDownloader initialized")
            
            self.video_analyzer = VideoAnalyzer()
            print("✓ VideoAnalyzer initialized")
            
            self.face_tracker = FaceTracker()
            print("✓ FaceTracker initialized")
            
            self.speaker_diarization = SpeakerDiarization()
            print("✓ SpeakerDiarization initialized")
            
            self.subtitle_generator = SubtitleGenerator()
            print("✓ SubtitleGenerator initialized")
            
            self.video_editor = VideoEditor()
            print("✓ VideoEditor initialized")
            
            self.utils = Utils()
            print("✓ Utils initialized")
            
        except Exception as e:
            print(f"Error initializing modules: {e}")
            messagebox.showerror("Initialization Error", f"Failed to initialize modules: {e}")
            raise
        
        print("Setting up UI...")
        self.setup_ui()
        print("SmartclipAI initialized successfully!")
        
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
        
        self.output_dir_var = tk.StringVar(value=str(OUTPUT_DIR))
        self.output_dir_entry = ctk.CTkEntry(
            dir_button_frame, 
            textvariable=self.output_dir_var,
            state="readonly"
        )
        self.output_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        output_browse_button = ctk.CTkButton(
            dir_button_frame,
            text="Browse",
            command=self.browse_output_dir,
            width=100
        )
        output_browse_button.pack(side="right")
        
        # Quality and format settings
        quality_frame = ctk.CTkFrame(output_frame)
        quality_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Left side - Quality
        quality_left = ctk.CTkFrame(quality_frame)
        quality_left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        quality_label = ctk.CTkLabel(quality_left, text="Kualitas Video:")
        quality_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.quality_var = tk.StringVar(value="720p")
        quality_menu = ctk.CTkOptionMenu(
            quality_left,
            variable=self.quality_var,
            values=["480p", "720p", "1080p", "1440p", "4K"]
        )
        quality_menu.pack(fill="x", padx=10, pady=(0, 10))
        
        # Right side - Format
        format_right = ctk.CTkFrame(quality_frame)
        format_right.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        format_label = ctk.CTkLabel(format_right, text="Format Output:")
        format_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.format_var = tk.StringVar(value="mp4")
        format_menu = ctk.CTkOptionMenu(
            format_right,
            variable=self.format_var,
            values=["mp4", "avi", "mov", "mkv"]
        )
        format_menu.pack(fill="x", padx=10, pady=(0, 10))
        
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
        
        # Estimated time
        self.time_estimate = ctk.CTkLabel(
            progress_frame,
            text="Perkiraan waktu: -",
            font=ctk.CTkFont(size=11),
            text_color="gray70"
        )
        self.time_estimate.pack(anchor="w", padx=20, pady=(0, 20))
        
    def setup_control_buttons(self):
        """Setup control buttons"""
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(fill="x", pady=(0, 20))
        
        # Button container
        button_container = ctk.CTkFrame(button_frame)
        button_container.pack(expand=True, pady=20)
        
        # Start processing button
        self.start_button = ctk.CTkButton(
            button_container,
            text="🚀 Mulai Proses AI",
            command=self.start_processing,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=200
        )
        self.start_button.pack(side="left", padx=10)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            button_container,
            text="⏹️ Stop",
            command=self.stop_processing,
            font=ctk.CTkFont(size=16),
            height=50,
            width=120,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        # Reset button
        self.reset_button = ctk.CTkButton(
            button_container,
            text="🔄 Reset",
            command=self.reset_form,
            font=ctk.CTkFont(size=16),
            height=50,
            width=120
        )
        self.reset_button.pack(side="left", padx=10)
        
    def setup_status_bar(self):
        """Setup status bar"""
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.pack(fill="x", side="bottom")
        
        self.status_text = ctk.CTkLabel(
            status_frame,
            text="✅ Siap - Masukkan URL YouTube atau pilih file video lokal",
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
            
    def browse_output_dir(self):
        """Browse untuk memilih folder output"""
        directory = filedialog.askdirectory(
            title="Pilih Folder Output",
            initialdir=self.output_dir_var.get()
        )
        
        if directory:
            self.output_dir_var.set(directory)
            self.update_status(f"Folder output: {directory}")
            
    def start_processing(self):
        """Mulai proses AI"""
        # Validate input
        url = self.url_entry.get().strip()
        file_path = self.file_path_var.get().strip()
        
        if not url and not file_path:
            messagebox.showerror("Error", "Masukkan URL YouTube atau pilih file video!")
            return
            
        if url and file_path:
            messagebox.showerror("Error", "Pilih salah satu: URL YouTube atau file lokal!")
            return
            
        # Disable controls
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Start processing in thread
        self.is_processing = True
        processing_thread = threading.Thread(
            target=self.process_video,
            args=(url if url else file_path, url != "")
        )
        processing_thread.daemon = True
        processing_thread.start()
        
    def stop_processing(self):
        """Stop proses AI"""
        self.is_processing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.update_status("❌ Proses dihentikan oleh pengguna")
        self.update_progress(0, "Proses dibatalkan")
        
    def reset_form(self):
        """Reset form ke kondisi awal"""
        # Clear inputs
        self.url_entry.delete(0, 'end')
        self.file_path_var.set("")
        
        # Reset progress
        self.progress_var.set(0)
        self.progress_text.configure(text="Siap untuk memproses...")
        self.time_estimate.configure(text="Perkiraan waktu: -")
        
        # Reset status
        self.update_status("✅ Form direset - Siap untuk input baru")
        
        # Enable controls
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
    def process_video(self, input_source, is_url=True):
        """Main processing function"""
        try:
            start_time = time.time()
            
            # Step 1: Download or load video
            if is_url:
                self.update_progress(10, "📥 Mengunduh video dari YouTube...")
                try:
                    video_path = self.youtube_dl.download(input_source)
                except Exception as e:
                    self.update_status(f"Error downloading: {e}")
                    return
            else:
                self.update_progress(10, "📂 Memuat file video...")
                video_path = input_source
                
            if not video_path or not self.is_processing:
                return
                
            # Step 2: Analyze video for best moments
            moments = None
            if self.detect_moments.get():
                self.update_progress(25, "🎯 Menganalisis moment terbaik dengan AI...")
                try:
                    moments = self.video_analyzer.analyze_video(video_path)
                except Exception as e:
                    self.update_status(f"Warning: Video analysis failed - {e}")
                    moments = None
                
            if not self.is_processing:
                return
                
            # Step 3: Face tracking
            face_data = None
            if self.face_tracking.get():
                self.update_progress(40, "👤 Melakukan face tracking...")
                try:
                    face_data = self.face_tracker.track_faces(video_path)
                except Exception as e:
                    self.update_status(f"Warning: Face tracking failed - {e}")
                    face_data = None
                
            if not self.is_processing:
                return
                
            # Step 4: Speaker diarization
            speaker_data = None
            if self.speaker_detection.get():
                self.update_progress(55, "🎙️ Mengidentifikasi pembicara...")
                try:
                    speaker_data = self.speaker_diarization.identify_speakers(video_path)
                except Exception as e:
                    self.update_status(f"Warning: Speaker diarization failed - {e}")
                    speaker_data = None
                
            if not self.is_processing:
                return
                
            # Step 5: Generate subtitles
            subtitle_data = None
            if self.auto_subtitle.get():
                self.update_progress(70, "📝 Menggenerate subtitle otomatis...")
                try:
                    subtitle_data = self.subtitle_generator.generate_subtitles(video_path)
                except Exception as e:
                    self.update_status(f"Warning: Subtitle generation failed - {e}")
                    subtitle_data = None
                
            if not self.is_processing:
                return
                
            # Step 6: Video editing and output
            self.update_progress(85, "🎬 Mengedit dan memproses video final...")
            
            output_options = {
                'moments': moments,
                'face_data': face_data,
                'speaker_data': speaker_data,
                'subtitle_data': subtitle_data,
                'add_watermark': self.add_watermark.get(),
                'podcast_mode': self.podcast_mode.get(),
                'quality': self.quality_var.get(),
                'format': self.format_var.get(),
                'output_dir': self.output_dir_var.get()
            }
            
            try:
                output_files = self.video_editor.process_video(video_path, output_options)
            except Exception as e:
                self.update_status(f"Error in video editing: {e}")
                output_files = []
            
            if not self.is_processing:
                return
                
            # Step 7: Cleanup and finish
            self.update_progress(100, "✅ Proses selesai!")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Show completion message
            self.show_completion_dialog(output_files, total_time)
            
        except Exception as e:
            if self.is_processing:
                self.update_status(f"❌ Error: {str(e)}")
                messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
                print(f"Detailed error: {e}")  # For debugging
                import traceback
                traceback.print_exc()
        finally:
            # Reset controls
            if self.is_processing:
                self.start_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                self.is_processing = False
                
    def update_progress(self, percentage, message):
        """Update progress bar dan message"""
        self.root.after(0, lambda: self._update_progress_ui(percentage, message))
        
    def _update_progress_ui(self, percentage, message):
        """Update UI progress (run in main thread)"""
        self.progress_var.set(percentage / 100.0)
        self.progress_text.configure(text=message)
        
        # Update time estimate
        if percentage > 0 and hasattr(self, 'process_start_time'):
            elapsed = time.time() - self.process_start_time
            estimated_total = elapsed / (percentage / 100.0)
            remaining = estimated_total - elapsed
            
            if remaining > 0:
                try:
                    remaining_str = self.utils.format_duration(remaining)
                    self.time_estimate.configure(text=f"Perkiraan waktu tersisa: {remaining_str}")
                except:
                    self.time_estimate.configure(text="Menghitung...")
            else:
                self.time_estimate.configure(text="Hampir selesai...")
        
    def update_status(self, message):
        """Update status bar"""
        self.root.after(0, lambda: self.status_text.configure(text=message))
        
    def show_completion_dialog(self, output_files, processing_time):
        """Show completion dialog"""
        try:
            time_str = self.utils.format_duration(processing_time)
        except:
            time_str = f"{processing_time:.1f} seconds"
        
        message = f"🎉 Proses selesai dalam {time_str}!\n\n"
        message += "File output yang dihasilkan:\n"
        
        if output_files:
            for file_path in output_files:
                message += f"• {Path(file_path).name}\n"
        else:
            message += "• Video processing completed\n"
            
        message += f"\nLokasi: {self.output_dir_var.get()}"
        
        messagebox.showinfo("Proses Selesai", message)
        
        # Ask if want to open output folder
        if messagebox.askyesno("Buka Folder", "Ingin membuka folder output?"):
            try:
                self.utils.open_folder(self.output_dir_var.get())
            except:
                # Fallback for opening folder
                import subprocess
                import platform
                if platform.system() == "Windows":
                    subprocess.Popen(f'explorer "{self.output_dir_var.get()}"')
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(["open", self.output_dir_var.get()])
                else:  # Linux
                    subprocess.Popen(["xdg-open", self.output_dir_var.get()])
            
    def run(self):
        """Run the application"""
        # Set process start time
        self.process_start_time = time.time()
        
        # Start main loop
        self.root.mainloop()

def main():
    """Main function"""
    try:
        print("Starting Smartclip AI...")
        app = SmartclipAI()
        print("Application initialized successfully")
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