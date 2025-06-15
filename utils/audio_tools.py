from pydub import AudioSegment, effects
import math
import os

def volume_multiplier_to_db(multiplier):
    if multiplier <= 0:
        raise ValueError("Multiplier must be > 0")
    return 20 * math.log10(multiplier)

def process_audio(file_path, multiplier, compress=False, dominance=False):
    audio = AudioSegment.from_file(file_path)
    db_increase = volume_multiplier_to_db(multiplier)
    louder = audio + db_increase
    louder = effects.normalize(louder)
    if compress:
        louder = louder.set_frame_rate(32000).compress_dynamic_range()
    if dominance:
        louder = louder.set_channels(1).set_frame_rate(16000)
    output_path = (
        file_path.replace(".mp3", "_boosted.raw")
        .replace(".opus", "_boosted.raw")
        .replace(".m4a", "_boosted.raw")
    )
    louder.export(output_path, format="raw")
    return output_path
