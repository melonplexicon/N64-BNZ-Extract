import os
import zlib

# Gets name of the ROM by cracking open the ROM and finding a string starting at whatever start_column is set to
# and then hopefully stops when it gets do non-text data and sets that as the filename. Just a straight conversion
# would give file names formatted like "N-####_e.z64" which work but it's not the prettiest. This way also isn't the
# prettiest but it's easier to go and rename if you have some immediate and blatant clue of what game the ROM is for
# without openning it in an emulator, hex editor, or comparing its hash.
def find_end_of_string(data, start):
    for i in range(start, len(data)):
        if not chr(data[i]).isprintable():
            return i
    return len(data)

def extract_name(data):
    start_column = 32 # Hopefully this is consistent across N64 games
    end_column = find_end_of_string(data, start_column)
    extracted_name = data[start_column:end_column].decode("cp1252").strip()
    return extracted_name

def decompress_and_rename(folderpath):
    try:
        for filename in os.listdir(folderpath):
            if filename.lower().endswith('.bnz'):
                inputfile = os.path.join(folderpath, filename)
                print(f"Processing {inputfile}")
                with open(inputfile, 'rb') as filein:
                    compresseddata = filein.read()
                try:
                    decompresseddata = zlib.decompress(compresseddata) # Decompress the bnz file
                    extracted_name = extract_name(decompresseddata) # Get the name of the game from the ROM
                    print(f"Extracted Name: {extracted_name}")
                    new_filename = extracted_name + '.z64' # idk if there's any meaningful reason to use one N64 exention or another, I'm just using z64 because that's the one I've seen the most
                    new_outputfile = os.path.join(folderpath, new_filename)
                    with open(new_outputfile, 'wb') as fileout:
                        fileout.write(decompresseddata)
                    print(f"Renamed to: {new_filename}")
                except zlib.error:
                    print("Decompression error.")
                    continue
    except FileNotFoundError:
        print("Folder not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    folderpath = input("Enter folder with bnz files: ") # folderpath should be formatted like "C:\Users\Melonplex\Desktop"
    decompress_and_rename(folderpath)                   # Do not include the quotes, I'm pretty sure that breaks it
    input("Press Enter to exit...")                     # I also don't know if forward slashes work like if you're using Linux--I also don't know if this even works on Linux
                                                        # I don't care enough to test it
