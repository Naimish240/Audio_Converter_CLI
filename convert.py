import os
import click
import platform
from tqdm import tqdm
from pydub import AudioSegment

def get_audio_files(folder, from_format) -> list:
    files = []
    for file in os.listdir(folder):
        for format in from_format:
            if file.endswith("."+format):
                files.append(file)

    return files

def convert_file(from_format, to_format, file, output_folder):
    if platform.system() == 'Windows':
        file_name = file.split('\\')[-1]
        file_name = output_folder + '\\' + file_name.split('.')[0] + '.' + to_format
    else:
        file_name = file.split('/')[-1]
        file_name = output_folder + file_name.split('.')[0] + '.' + to_format

    track = AudioSegment.from_file(file, format=from_format)
    track.export(file_name, format=to_format)


@click.command()
@click.option(
    "--input_path",
    prompt="Path to load audio files from: ",
    default="audios/",
    help="Enter the path to load all audio files for conversion"
)
@click.option(
    "--output_path",
    prompt="Path to save converted audio files to: ",
    default="converted_audios/",
    help="Enter the path to save all audio files after conversion to"
)
@click.option(
    "--from_format",
    prompt="File formats you want to process (space seperated): ",
    default="all",
    help="Options: [mp3, ogg, wma, aac, flv, m4a, wav, all]"
)
@click.option(
    "--to_format",
    prompt="File format to convert audios into: ",
    default="mp3",
    help="Options (select ONE): [mp3, ogg, wma, aac, flv, m4a, wav]"
)
def main(input_path, output_path, from_format, to_format):

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    if from_format == 'all':
        from_format = ['mp3', 'ogg', 'wma', 'aac', 'flv', 'm4a', 'wav']
    else:
        from_format = from_format.split()

    print("... Indexing Folder", input_path)
    files = get_audio_files(input_path, from_format)
    print("... Found", len(files), "matching audio files in folder.")

    print("... Converting Files.")
    for i in tqdm(range(len(files))):
        file = input_path + files[i]
        file_format = file.split('.')[1]
        convert_file(file_format, to_format, file, output_path)
    print("... Finished Converting Files!")

    print("... Exitting Program.")


if __name__ == '__main__':
    main()