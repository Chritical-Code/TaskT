import simpleaudio as sa

class Sound:
    def __init__(self):
        self.nav = sa.WaveObject.from_wave_file("sound/navigateL.wav")
        self.bac = sa.WaveObject.from_wave_file("sound/back.wav")
        self.sel = sa.WaveObject.from_wave_file("sound/select.wav")
        self.com = sa.WaveObject.from_wave_file("sound/complete.wav")
    
    def PlaySound(self, inSound):
        if inSound == "nav":
            play_obj = self.nav.play()
        if inSound == "bac":
            play_obj = self.bac.play()
        if inSound == "sel":
            play_obj = self.sel.play()
        if inSound == "com":
            play_obj = self.com.play()
        
        return play_obj