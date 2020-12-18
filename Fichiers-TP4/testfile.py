import simpleaudio




filename = "son/sf_laser_15.wav"
 
sound_object = simpleaudio.WaveObject.from_wave_file(filename)
play_object = sound_object.play()
play_object.wait_done()