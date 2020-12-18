import simpleaudio




filename = "son/sf_laser_15.wav"
 
sound_object = simpleaudio.WaveObject.from_wave_file(filename)
sound_object.play()



boutondefaite = self.sonexplosion
wave_obj = sa.WaveObject.from_wave_file(boutondefaite)
wave_obj.play()