from pydub import AudioSegment

audioSegList = []
audioSegList.append(AudioSegment.from_file("../resources/Myotis ikonnikovi.WAV","wav"))
audioSegList.append(AudioSegment.from_file("../resources/bat.wav","wav"))
audioSegList.append(AudioSegment.from_file("../resources/Pipistrellus abramus.WAV","wav"))
#audioSegList.append(AudioSegment.from_file("../resources/죽전동 맹꽁이 한마리 2020_07_22_16_16_31.mp3","mp3"))

combined = AudioSegment.empty()
for song in audioSegList:
    combined += song

#combined.export("../resources/concatTest.wav", format="wav")   #o
#combined.export("../resources/concatTest.mp3", format="mp3")   #o
#combined.export("../resources/concatTest.m4a", format="m4a")   #x
#combined.export("../resources/concatTest.flac", format="flac")  #o
#combined.export("../resources/concatTest.mp4", format="mp4")    #o
#combined.export("../resources/concatTest.wma", format="wma")    #x
combined.export("../resources/concatTest.aac", format="aac")    #x



