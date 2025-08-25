# ascii art and sonification

> ## about
> 
> this is the repository to keep track of my work on my BSc thesis  
> this is to be reworked later in a different language as separate projects

> ## status report
> 
> implementation: rushed, janky, ***done***

> ## features implemented
> 
> - ascii art generation
>   - customizable ascii art generation rules with presets
>     - font size
>     - character set / inversion
>     - edge detection / parameters
>       -  realistic ascii conversion of edges
>     - text and background color
>    -  real time display of results
>    -  copy as text to clipboard
> - sonification 
>   - customizable sonification (image to sound) rules with presets
>     - custom scales
>     - octave ranges
>     - image processing settings
>       - grid rows and columns
>       - pitch mapping normalization
>       - custom velocity mapping / range
>       - use rgb channels of image to make chords
>       - merge adjacent notes into one long note
>   - real time playback and visualization of the generated audio/midi
>     -  bpm
>     -  midi instruments
>     -  stepchart with real time indicator
>     -  grid on the image with real time highlighting
>   - download as midi
> - sleek streamlit ui for both

# how to run the app

### create a virtual environment
for macos/linux:
> python3 -m venv venv  
> source venv/bin/activate

for windows:
> python -m venv venv  
> .\venv\Scripts\activate

### install dependencies
> pip install -r requirements.txt

### run the app
> streamlit run main_app.py
