
![](https://i.imgur.com/UBk22y8.png)
![GitHub last commit](https://img.shields.io/github/last-commit/smolikja/voicetelling) ![GitHub Release Date](https://img.shields.io/github/release-date/smolikja/voicetelling)
# Voicetelling
Voicetelling is a script merging (=grouping, combining) Facebook Messenger voice messages by day into .mp3 files.

- Voice messages are merged by date they have been created into .mp3 audio files.
- Set the date range for which voice messages will be processed.
- Output files are located in script created `export` folder.
- Each day for the script starts at 5.00AM.

## Windows setup
Make sure you have [FFmpeg](https://www.ffmpeg.org/download.html) installed in your system.

> tip: Install via [Chocolatey](https://chocolatey.org/install) `choco install ffmpeg`

Download latest executable from [releases](https://github.com/smolikja/voicetelling/releases).

## How to use
1. [Request and download](https://www.facebook.com/help/212802592074644)  your Facebook messages:
`facebook.com > Settings & Privacy > Settings > Your Facebook Information > Donwload Your Information > thic Messages`

2. Copy `voicetelling.exe` and paste it into `/facebook-{user}/messages/ibox/{conversation}/audio`

3. Run `voicetelling.exe`

	>optional: set date range

4. Exported files are located in `/facebook-{user}/messages/ibox/{conversation}/audio/export`

## Example
TODO: video

## Contribution
All contributions are welcomed!

Make sure, you have [Python](https://www.python.org/downloads/), [ FFmpeg](https://www.ffmpeg.org/download.html), [Pydub](https://github.com/jiaaro/pydub) in your system installed.
Fork repository and contribute:))


## TODO
- multithreading