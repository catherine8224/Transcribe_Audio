# Transcribe_Audio
An audio transcription website that relies on speech-to-text algorithms that will convert audio &amp; video files to text in minutes. Currently does not support speaker diarization.
```diff
- Currently had an issue with google cloud storage. Will resolve soon. Has been updated to support audio transcription for more than 30 seconds, and will be updated for speaker diarization
```
## WEBSITE
https://www.speechanalyzer.me/
<hr>
<h3> About Speech Analyzer </h3>
<p font-size: > Speech Analyzer is a micro web framework written in Python.</p>
<p> Speech Analyzer is a web application that can take in pre-recorded audio files (wav, mp3, m4a, ogg and FLAC)</p>
<p> You can either do two things: 1) upload one/multiple audio file(s) or 2) upload a Youtube music video with captions so that it can process the captioned words. 
      <ol>
      <li>
      For the first option, it can take in audio files in different languages (French, Spanish, Chinese, and English). Once it is processed and saved in Google Cloud Storage, it will transcribe the audio, and create a Word Cloud and bar graph of the words said in the file. 
      I have used Seaborn, matplotlib, and plot.ly to generate the bar graphs. We hope to continue editing this website so that it can process music. </li>
      <li>
      The second option uses the YouTube API to scrape the captions of the music videos on YouTube. It will then create a Word Cloud and bar graph of the words said in the file. </li>
    </ol>
<p>You can contact us in the "Contact Us" link if there are any issues. </p>
    <b> What is FLAC?</b>
    <p> It stands for Free Lossless Audio Codec.It is compatible with many phones (including the iPhone -- with an app), portable music players (PMP) including the PonoPlayer and hi-fi components. 
      FLAC files are available for roughly the same price as the equivalent MP3 in online stores and sound much better. Be sure that your flac files are complete, and has the usual MD5 signature. 
      If you get this when typing flac -st [output.flac]: output.flac: WARNING, cannot check MD5 signature since it was unset in the STREAMINFO, 
      then you may have to re-record your audio. 
    </p>
    <b> What is WAV? </b>
    <p>A WAV file is a raw audio format created by Microsoft and IBM. The format uses containers to store audio data, track numbers, sample rate, and bit rate. WAV files are uncompressed lossless audio 
      and as such can take up quite a bit of space, coming in around 10 MB per minute with a maximum file size of 4 GB.</p>
    <b>What is MP3?</b> 
    <p> MP3 is a lossy format, which means parts of the music are shaved off to reduce the file size to a more compact level. It is supposed to use "psychoacoustics" to delete overlapping sounds, 
      but it isn't always successful. Typically, cymbals, reverb and guitars are the sounds most affected by MP3 compression and can sound really distorted or "crunchy" when too much compression is applied.</p>
    <b> What is M4A? </b>
    <p> It is a file extension for an audio file encoded with advanced audio coding (AAC) which is a lossy compression.</p>
    <b> What is OGG? </b>
    <p>Ogg is a free, open container format It allows users to stream and alter high quality digital multimedia files. The name “Ogg” derives from the jargon word “ogging.” Ogging refers to the killing of a carrier 
      by a suicide run in the game Netrek. Apple does not support OGG file formats, and the presence of more common and widely compatible formats like MP3 mean the OGG file is not that frequently distributed in the digital media world. </p>
  
 Note: The Recorder produces a mono (1-channel) recording in .ogg format. 
    </div>
