from pygame import mixer
import os

class SoundPlayer:
    """ The SoundPlayer class is responsible for playing sounds in the game

       The class has the following attributes:
           - sound: The sound to be played
           - is_music: A flag indicating whether the sound is music or a sound effect
    """

    def __init__(self,sound_name,is_music)-> None:
        """ 
            Initializes a new instance of the SoundPlayer class and calls the load_sound method to load the sound file
            
            Args:
                - sound_name (str): The name of the sound file to be played
                - is_music (bool): A flag indicating whether the sound is music or a sound effect
        """

        mixer.init()

        self.is_music = is_music

        self.load_sound(sound_name)

    def load_sound(self,sound_name):
        """ The load_sound method is responsible for loading the sound file to be played
        
            Args:
                - sound_name (str): The name of the sound file to be loaded
        """

        if self.is_music:
            sound_path = os.path.join(os.path.dirname(__file__), f"../Assets/SoundTrack/Music/{sound_name}.wav")
        else:
            sound_path = os.path.join(os.path.dirname(__file__), f"../Assets/SoundTrack/SoundEffects/{sound_name}.wav")

        self.sound = mixer.Sound(sound_path)

    def play(self):
        """ The play method is responsible for playing the sound and setting the volume, and looping the sound if it is music
        """
        self.sound.set_volume(0.1)

        loop = -1 if self.is_music else 0

        self.sound.play(loop)
     