# core/voice/voice_control.py
import speech_recognition as sr
import pyttsx3
from typing import Dict, Optional
import asyncio

class VoiceControl:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.wake_word = "sam"
        self.commands = {
            "lights": self.control_lights,
            "temperature": self.control_temperature,
            "status": self.get_status,
            "analytics": self.show_analytics
        }
        
    async def listen(self):
        """Listen for commands"""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            
        try:
            command = self.recognizer.recognize_google(audio).lower()
            if self.wake_word in command:
                await self.process_command(command)
        except Exception as e:
            print(f"Error: {e}")
            
    async def process_command(self, command: str):
        """Process voice command"""
        for key, func in self.commands.items():
            if key in command:
                await func()
                
    async def speak(self, text: str):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()

# core/visualization/renderer.py
import moderngl
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class VisualState:
    color: Tuple[float, float, float]
    position: Tuple[float, float, float]
    scale: float
    rotation: float

class Renderer3D:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.prog = self.load_shaders()
        self.vbo = self.create_buffers()
        self.state = VisualState(
            color=(0.0, 1.0, 0.0),
            position=(0.0, 0.0, 0.0),
            scale=1.0,
            rotation=0.0
        )
        
    def load_shaders(self):
        """Load and compile shaders"""
        vertex_shader = """
            #version 330
            in vec3 in_position;
            uniform mat4 mvp;
            void main() {
                gl_Position = mvp * vec4(in_position, 1.0);
            }
        """
        
        fragment_shader = """
            #version 330
            out vec4 fragColor;
            uniform vec3 color;
            void main() {
                fragColor = vec4(color, 1.0);
            }
        """
        
        return self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        
    def create_buffers(self):
        """Create vertex buffers"""
        vertices = np.array([
            # Front face
            -1.0, -1.0,  1.0,
             1.0, -1.0,  1.0,
             1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            # Back face
            -1.0, -1.0, -1.0,
            -1.0,  1.0, -1.0,
             1.0,  1.0, -1.0,
             1.0, -1.0, -1.0
        ], dtype='f4')
        
        return self.ctx.buffer(vertices.tobytes())
        
    def render(self):
        """Render frame"""
        self.ctx.clear(0.0, 0.0, 0.0, 0.0)
        
        # Update uniforms
        self.prog['mvp'].write(self.get_mvp_matrix())
        self.prog['color'].write(np.array(self.state.color, dtype='f4'))
        
        # Render
        self.vbo.bind()
        self.ctx.render_triangles()
        
    def get_mvp_matrix(self):
        """Calculate Model View Projection matrix"""
        # Implement matrix calculations here
        pass
