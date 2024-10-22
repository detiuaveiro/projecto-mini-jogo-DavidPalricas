from pygame import mixer

class SoundPlayer:
    """ A class to represent a sound player in the game
        It plays the background music and the sound effects
    """
    def __init__(self,sound_name,is_music):
        """ Constructor for the SoundPlayer class
            It initializes the sound
            
            Parameters: sound_name (stores the name of the sound to be played), is_music (stores a boolean value to check if the sound is a music or a sound effect)
        """
        mixer.init()

        self.is_music = is_music
        self.sound = mixer.Sound(f"../Assets/SoundTrack/Music/{sound_name}.wav") if self.is_music else mixer.Sound(f"../Assets/SoundTrack/SoundEffects/{sound_name}.wav")

    def play(self):
        """ Method to play the sound
            It plays the sound with a volume of 0.1 and loops the sound if it is a music
        """
        self.sound.set_volume(0.1)

        loop = -1 if self.is_music else 0

        self.sound.play(loop)
     