import customtkinter as ctk
import datetime
import google.generativeai as genai
import threading
from PIL import Image
import os
import io
from tkinter import filedialog # For file dialog to upload audio
load_dotenv()



try:
    import cairosvg # Required for SVG rendering
except ImportError:
    cairosvg = None # Set to None if not available

# --- Gemini API Configuration ---
api_key = os.getenv("GEMINI_API_KEY")
if api_key is None:
    raise ValueError("API key not found. Make sure 'YOUR_API_KEY' is set in your .env file.")




genai.configure(api_key=API_KEY)

# --- UI Theme Configuration ---
ctk.set_appearance_mode("light") # Keeping it bright
ctk.set_default_color_theme("blue") # A clean, modern blue theme

class DiaryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Red Hat Diary Tool - Prototype")
        self.geometry("850x780") # Adjusted size for new layout with bottom buttons
        self.minsize(700, 600)

        # Configure main window grid (Header + Main Content Area + Footer Buttons)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Main Content Area (input, AI response)
        self.grid_rowconfigure(2, weight=0) # All action buttons & status bar at the very bottom

        # --- Custom Fonts ---
        self.font_header = ctk.CTkFont(family="Inter", size=32, weight="bold")
        self.font_subheader = ctk.CTkFont(family="Inter", size=18, weight="bold") # Slightly smaller
        self.font_body = ctk.CTkFont(family="Inter", size=14)
        self.font_button = ctk.CTkFont(family="Inter", size=15, weight="bold")
        self.font_status = ctk.CTkFont(family="Inter", size=11, slant="italic") # Italic for status

        # --- Header Panel (Red Hat inspired) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="#CC0000", corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=0) # For logo/icon
        self.header_frame.grid_columnconfigure(1, weight=1) # For title

        # --- Red Hat Logo (Loading from local SVG/PNG file) ---
        logo_image_path = "redhat.svg"
        logo_fallback_path = "redhat.png"
        logo_size = (45, 45) # Slightly larger logo

        self.redhat_ctk_image = None

        try:
            image_loaded = False
            if os.path.exists(logo_image_path):
                if logo_image_path.lower().endswith(".svg"):
                    if cairosvg:
                        png_data = cairosvg.svg2png(url=logo_image_path, output_width=logo_size[0], output_height=logo_size[1])
                        logo_image = Image.open(io.BytesIO(png_data))
                        self.redhat_ctk_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=logo_size)
                        image_loaded = True
                    else:
                        print(f"Warning: cairosvg not installed. Cannot render SVG '{logo_image_path}'. Attempting PNG fallback.")
                elif logo_image_path.lower().endswith((".png", ".jpg", ".jpeg")):
                    logo_image = Image.open(logo_image_path).resize(logo_size, Image.LANCZOS)
                    self.redhat_ctk_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=logo_size)
                    image_loaded = True

            if not image_loaded and os.path.exists(logo_fallback_path):
                logo_image = Image.open(logo_fallback_path).resize(logo_size, Image.LANCZOS)
                self.redhat_ctk_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=logo_size)
                image_loaded = True

            if not image_loaded:
                raise FileNotFoundError(f"Neither '{logo_image_path}' nor '{logo_fallback_path}' found or could be loaded.")

            self.redhat_logo_label = ctk.CTkLabel(
                self.header_frame,
                image=self.redhat_ctk_image,
                text="",
                compound="left",
                pady=10
            )

        except (FileNotFoundError, ImportError, Exception) as e:
            fallback_text = "⚠️ Logo Missing"
            if isinstance(e, FileNotFoundError):
                fallback_text = f"⚠️ Logo Missing ({os.path.basename(logo_image_path)} / {os.path.basename(logo_fallback_path)})"
            elif isinstance(e, ImportError) and "cairosvg" in str(e):
                fallback_text = "⚠️ cairosvg missing"
            else:
                fallback_text = f"❌ Logo Error: {e}"

            self.redhat_logo_label = ctk.CTkLabel(
                self.header_frame,
                text=fallback_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white",
                pady=10
            )
            print(f"Error loading logo: {e}. Displaying text fallback.")

        self.redhat_logo_label.grid(row=0, column=0, padx=(30, 10), pady=10, sticky="w")

        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Red Hat Diary Tool",
            font=self.font_header,
            text_color="white",
            pady=10
        )
        self.header_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # --- Main Content Area (Unified Single Column for Textbox & AI Response) ---
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#F0F0F0") # A very light gray background
        self.main_content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.main_content_frame.grid_columnconfigure(0, weight=1) # Single column for all inner elements
        self.main_content_frame.grid_rowconfigure(0, weight=1) # Input Textbox (takes available space)
        self.main_content_frame.grid_rowconfigure(1, weight=1) # AI Response Textbox (takes available space)


        # Input Section
        self.welcome_label = ctk.CTkLabel(
            self.main_content_frame,
            text="Write Your Thoughts Here:",
            font=self.font_subheader,
            text_color="#CC0000"
        )
        self.welcome_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.entry_textbox = ctk.CTkTextbox(
            self.main_content_frame,
            height=120, # Initial height, will stretch with weight=1
            font=self.font_body,
            wrap="word",
            border_width=2,
            corner_radius=8,
            border_color="#CC0000",
            fg_color="white" # Explicitly white background for textbox
        )
        self.entry_textbox.grid(row=0, column=0, padx=20, pady=(5, 10), sticky="nsew")

        self.placeholder_text = "Start typing your diary entry here... (or record/upload audio below)"
        self.is_placeholder_active = True
        self._insert_placeholder()

        self.entry_textbox.bind("<FocusIn>", self._on_focus_in)
        self.entry_textbox.bind("<FocusOut>", self._on_focus_out)
        self.entry_textbox.bind("<Key>", self._on_key_press)
        self.entry_textbox.bind("<Control-a>", self._select_all_text)
        self.entry_textbox.bind("<Command-a>", self._select_all_text)

        # AI Response Display Section
        self.ai_response_label = ctk.CTkLabel(
            self.main_content_frame,
            text="AI Response:",
            font=self.font_subheader,
            text_color="#CC0000"
        )
        self.ai_response_label.grid(row=1, column=0, padx=20, pady=(15, 5), sticky="w") # Now in row 1

        self.display_textbox = ctk.CTkTextbox(
            self.main_content_frame,
            height=150, # Initial height, will stretch with weight=1
            font=self.font_body,
            wrap="word",
            state="disabled",
            border_width=2,
            corner_radius=8,
            border_color="#0066CC",
            fg_color="white"
        )
        self.display_textbox.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="nsew") # Now in row 1
        self.display_textbox.configure(state="normal")
        self.display_textbox.insert("0.0", "AI responses will appear here after you click 'Ask AI'.")
        self.display_textbox.configure(state="disabled")


        # --- Bottom Action Bar (New Frame for all buttons and status) ---
        self.bottom_action_bar = ctk.CTkFrame(self, fg_color=self.cget("fg_color"), corner_radius=0) # Match main window background
        self.bottom_action_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.bottom_action_bar.grid_columnconfigure(0, weight=1) # General area for buttons
        self.bottom_action_bar.grid_rowconfigure(0, weight=0) # Audio path
        self.bottom_action_bar.grid_rowconfigure(1, weight=0) # Main action buttons
        self.bottom_action_bar.grid_rowconfigure(2, weight=0) # AI action buttons
        self.bottom_action_bar.grid_rowconfigure(3, weight=0) # Status label

        # Audio Filepath Display (moved to bottom bar)
        self.audio_filepath_textbox = ctk.CTkTextbox(
            self.bottom_action_bar,
            height=30, # Smaller height
            font=self.font_body,
            wrap="word",
            state="disabled",
            border_width=1,
            corner_radius=8,
            border_color="#DDDDDD",
            fg_color="white"
        )
        self.audio_filepath_textbox.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.audio_filepath_textbox.configure(state="normal")
        self.audio_filepath_textbox.delete("0.0", "end")
        self.audio_filepath_textbox.insert("0.0", "No audio file selected.")
        self.audio_filepath_textbox.configure(state="disabled")

        # Main Action Buttons (Add Entry, Ask AI, Record, Upload)
        self.all_buttons_frame = ctk.CTkFrame(self.bottom_action_bar, fg_color="transparent")
        self.all_buttons_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.all_buttons_frame.grid_columnconfigure(0, weight=1) # Add Entry
        self.all_buttons_frame.grid_columnconfigure(1, weight=1) # Ask AI
        self.all_buttons_frame.grid_columnconfigure(2, weight=1) # Record
        self.all_buttons_frame.grid_columnconfigure(3, weight=1) # Upload

        self.add_button = ctk.CTkButton(
            self.all_buttons_frame,
            text="Add Entry",
            command=self._add_entry,
            font=self.font_button,
            fg_color="#CC0000",
            hover_color="#A50000",
            text_color="white",
            corner_radius=8,
            height=40
        )
        self.add_button.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        self.ask_ai_button = ctk.CTkButton(
            self.all_buttons_frame,
            text="Ask AI",
            command=self._ask_ai,
            font=self.font_button,
            fg_color="#0066CC",
            hover_color="#004C99",
            text_color="white",
            corner_radius=8,
            height=40
        )
        self.ask_ai_button.grid(row=0, column=1, padx=(5, 5), pady=0, sticky="ew")
        
        self.is_recording = False # State flag for recording
        self.record_button = ctk.CTkButton(
            self.all_buttons_frame,
            text="● Record Audio", # Red dot for recording
            command=self._toggle_record, # Now toggles record/stop
            font=self.font_button,
            fg_color="red", # Red for record
            hover_color="#A50000",
            text_color="white",
            corner_radius=8,
            height=40
        )
        self.record_button.grid(row=0, column=2, padx=(5, 5), pady=0, sticky="ew")
        
        self.upload_audio_button = ctk.CTkButton(
            self.all_buttons_frame,
            text="↑ Upload Audio", # Up arrow for upload
            command=self._upload_audio_file, # New function for file dialog
            font=self.font_button,
            fg_color="#0066CC", # Blue for upload
            hover_color="#004C99",
            text_color="white",
            corner_radius=8,
            height=40
        )
        self.upload_audio_button.grid(row=0, column=3, padx=(5, 0), pady=0, sticky="ew")

        # AI Action Buttons (OK/Discard) - now also in the bottom bar
        self.ai_action_buttons_frame = ctk.CTkFrame(self.bottom_action_bar, fg_color="transparent")
        self.ai_action_buttons_frame.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.ai_action_buttons_frame.grid_columnconfigure(0, weight=1)
        self.ai_action_buttons_frame.grid_columnconfigure(1, weight=1)

        self.ok_button = ctk.CTkButton(
            self.ai_action_buttons_frame,
            text="✓ OK (Save AI Response)", # Checkmark for OK
            command=self._confirm_ai_entry,
            font=self.font_button,
            fg_color="green",
            hover_color="#006400",
            text_color="white",
            corner_radius=8,
            height=40
        )
        self.ok_button.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="ew")
        self.ok_button.grid_remove() # Initially hide

        self.discard_button = ctk.CTkButton(
            self.ai_action_buttons_frame,
            text="✗ Discard AI Response", # Cross for Discard
            command=self._discard_ai_entry,
            font=self.font_button,
            fg_color="red",
            hover_color="#8B0000",
            text_color="white",
            corner_radius=8,
            height=40
        )
        self.discard_button.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="ew")
        self.discard_button.grid_remove() # Initially hide

        # Status Label (at the very bottom of the bottom bar)
        self.status_label = ctk.CTkLabel(
            self.bottom_action_bar,
            text="",
            font=self.font_status,
            text_color="gray"
        )
        self.status_label.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="w")

    # --- End of __init__ method ---

    # --- Class methods (rest of your methods remain unchanged) ---
    def _insert_placeholder(self):
        self.entry_textbox.delete("0.0", "end")
        self.entry_textbox.insert("0.0", self.placeholder_text)
        self.entry_textbox.configure(text_color="gray")
        self.is_placeholder_active = True

    def _remove_placeholder(self):
        if self.is_placeholder_active:
            self.entry_textbox.delete("0.0", "end")
            self.is_placeholder_active = False

    def _on_focus_in(self, event):
        self._remove_placeholder()

    def _on_focus_out(self, event):
        if not self.entry_textbox.get("0.0", "end").strip():
            self._insert_placeholder()

    def _on_key_press(self, event):
        if self.is_placeholder_active:
            self._remove_placeholder()

    def _add_entry(self):
        entry_content = self.entry_textbox.get("0.0", "end").strip()

        if entry_content == self.placeholder_text or not entry_content:
            self.status_label.configure(text="Please type an entry first.", text_color="orange")
        else:
            try:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_entry = (
                    f"------------------{current_time}----------------------\n"
                    f"{entry_content}\n"
                    f"-----------------------------------------------------------\n\n"
                )
                with open("diary.txt", "a") as f:
                    f.write(formatted_entry)

                self.status_label.configure(text=f"Entry added to diary.txt: '{entry_content[:50]}...'")
                self.status_label.configure(text_color="green")
                self.entry_textbox.delete("0.0", "end")
                self._insert_placeholder()
            except IOError as e:
                self.status_label.configure(text=f"Error writing to file: {e}", text_color="red")

        self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))

    def _ask_ai(self):
        input_text = self.entry_textbox.get("0.0", "end").strip()
        audio_file_path = self.audio_filepath_textbox.get("0.0", "end").strip()

        if (input_text == self.placeholder_text or not input_text) and \
           (not audio_file_path or audio_file_path == "No audio file selected."):
            self.status_label.configure(text="Enter text or select an audio file.", text_color="orange")
            self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))
            return

        self.status_label.configure(text="Asking AI... Please wait.", text_color="blue")
        self.display_textbox.configure(state="normal")
        self.display_textbox.delete("0.0", "end")
        self.display_textbox.insert("0.0", "Generating AI response...")
        self.display_textbox.configure(state="disabled")

        self.ok_button.grid_remove()
        self.discard_button.grid_remove()

        threading.Thread(target=self._get_gemini_response, args=(input_text, audio_file_path)).start()

    def _get_gemini_response(self, user_input, audio_file_path):
        uploaded_file = None
        try:
            # Use gemini-1.5-flash for multimodal capabilities
            model = genai.GenerativeModel('gemini-1.5-flash') 

            contents = []
            if user_input and user_input != self.placeholder_text:
                contents.append(user_input)
            
            if audio_file_path and audio_file_path != "No audio file selected.":
                if not os.path.exists(audio_file_path):
                    raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
                
                self.after(0, lambda: self.status_label.configure(text=f"Uploading audio: {os.path.basename(audio_file_path)}...", text_color="blue"))
                
                # Upload the audio file to Gemini's file service
                # The mimeType should match the file's actual type (e.g., audio/wav, audio/mpeg for mp3)
                # For simplicity, we'll try to infer or use a common one.
                mime_type = "audio/mpeg" if audio_file_path.lower().endswith(".mp3") else "audio/wav"
                
                # Upload the file
                uploaded_file = genai.upload_file(path=audio_file_path, display_name=os.path.basename(audio_file_path))
                contents.append(uploaded_file)
                self.after(0, lambda: self.status_label.configure(text=f"Audio uploaded. Processing...", text_color="blue"))

            prompt_text = (
                "Based on the following input, provide a short professional summary in english, "
                "a list of technical skills used/gained (if any), and a list of soft skills used/gained (if any). "
                "Present each item on a new line."
            )
            
            # Combine prompt with user input and uploaded file data
            full_prompt_parts = [prompt_text, "Input:"] + contents
            
            response = model.generate_content(full_prompt_parts)
            ai_output = response.text
            self.after(0, self._update_ai_display, ai_output, None)
        except Exception as e:
            self.after(0, self._update_ai_display, None, str(e))
        finally:
            # Delete the uploaded file from Gemini's file service after use
            if uploaded_file:
                try:
                    genai.delete_file(uploaded_file.name)
                    print(f"Deleted uploaded file: {uploaded_file.display_name}")
                except Exception as delete_e:
                    print(f"Error deleting uploaded file {uploaded_file.display_name}: {delete_e}")


    def _update_ai_display(self, ai_output, error_message):
        self.display_textbox.configure(state="normal")
        self.display_textbox.delete("0.0", "end")

        if ai_output:
            self.display_textbox.insert("0.0", ai_output)
            self.status_label.configure(text="AI response generated.", text_color="green")
            self.ok_button.grid()
            self.discard_button.grid()
        elif error_message:
            self.display_textbox.insert("0.0", f"Error from AI: {error_message}")
            self.status_label.configure(text=f"AI Error: {error_message}", text_color="red")

        self.display_textbox.configure(state="disabled")
        self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))

    def _confirm_ai_entry(self):
        ai_response_content = self.display_textbox.get("0.0", "end").strip()

        if not ai_response_content or \
           ai_response_content == "AI responses will appear here after you click 'Ask AI'." or \
           "Error from AI:" in ai_response_content:
            self.status_label.configure(text="No valid AI response to save.", text_color="orange")
            self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))
            return

        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_entry = (
                f"--------------------------AI Generated - {current_time}----------------\n"
                f"{ai_response_content}\n"
                f"-------------------------------------------------------------------------\n\n"
            )
            with open("diary.txt", "a") as f:
                f.write(formatted_entry)

            self.status_label.configure(text="AI response saved to diary.txt!", text_color="green")
            self.display_textbox.configure(state="normal")
            self.display_textbox.delete("0.0", "end")
            self.display_textbox.insert("0.0", "AI responses will appear here after you click 'Ask AI'.")
            self.display_textbox.configure(state="disabled")
            self.ok_button.grid_remove()
            self.discard_button.grid_remove()
        except IOError as e:
            self.status_label.configure(text=f"Error saving AI response: {e}", text_color="red")

        self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))

    def _discard_ai_entry(self):
        self.status_label.configure(text="AI response discarded.", text_color="blue")
        self.display_textbox.configure(state="normal")
        self.display_textbox.delete("0.0", "end")
        self.display_textbox.insert("0.0", "AI responses will appear here after you click 'Ask AI'.")
        self.display_textbox.configure(state="disabled")
        self.ok_button.grid_remove()
        self.discard_button.grid_remove()
        self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))

    def _select_all_text(self, event=None):
        if not self.is_placeholder_active or self.entry_textbox.get("0.0", "end").strip() != self.placeholder_text:
            self.entry_textbox.tag_remove("sel", "1.0", "end")
            self.entry_textbox.tag_add("sel", "1.0", "end")
        return "break"

    def _toggle_record(self):
        if not self.is_recording:
            # Start recording (simulated)
            print("Recording audio... (Simulated)")
            self.status_label.configure(text="Recording... Click to stop.", text_color="red")
            self.record_button.configure(text="◼ Stop Recording", fg_color="red", hover_color="#8B0000")
            self.is_recording = True
            
            # Clear previous audio file path when starting a new recording
            self.audio_filepath_textbox.configure(state="normal")
            self.audio_filepath_textbox.delete("0.0", "end")
            self.audio_filepath_textbox.insert("0.0", "Recording in progress...")
            self.audio_filepath_textbox.configure(state="disabled")

        else:
            # Stop recording (simulated)
            print("Stopping recording... (Simulated)")
            self.status_label.configure(text="Recording stopped.", text_color="green")
            self.record_button.configure(text="● Record Audio", fg_color="#0066CC", hover_color="#004C99") # Revert color/text
            self.is_recording = False
            
            # Simulate a saved file path after stopping
            simulated_audio_path = "simulated_recording.wav" 
            self.audio_filepath_textbox.configure(state="normal")
            self.audio_filepath_textbox.delete("0.0", "end")
            self.audio_filepath_textbox.insert("0.0", simulated_audio_path)
            self.audio_filepath_textbox.configure(state="disabled")
            self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))

    def _upload_audio_file(self):
        if self.is_recording: # Prevent upload while recording is simulated
            self.status_label.configure(text="Cannot upload while recording is active. Stop recording first.", text_color="orange")
            self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))
            return

        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.flac"), ("All Files", "*.*")]
        )
        if file_path:
            self.audio_filepath_textbox.configure(state="normal")
            self.audio_filepath_textbox.delete("0.0", "end")
            self.audio_filepath_textbox.insert("0.0", file_path)
            self.audio_filepath_textbox.configure(state="disabled")
            self.status_label.configure(text=f"Audio file selected: {os.path.basename(file_path)}", text_color="green")
        else:
            self.status_label.configure(text="No audio file selected.", text_color="gray")
            # If nothing was selected, reset to default message in textbox if it was empty
            if not self.audio_filepath_textbox.get("0.0", "end").strip() or self.audio_filepath_textbox.get("0.0", "end").strip() == "Recording in progress...":
                 self.audio_filepath_textbox.configure(state="normal")
                 self.audio_filepath_textbox.delete("0.0", "end")
                 self.audio_filepath_textbox.insert("0.0", "No audio file selected.")
                 self.audio_filepath_textbox.configure(state="disabled")
        self.after(3000, lambda: self.status_label.configure(text="", text_color="gray"))


if __name__ == "__main__":
    app = DiaryApp()
    app.mainloop()
