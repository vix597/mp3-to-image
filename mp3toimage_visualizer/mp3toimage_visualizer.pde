/*
 * mp3toimage_visualizer.pde
 *
 * MP3 to image visualization sketch. Reads in
 * a .pb file generated with Python and plays
 * it back here. (song file must exist in
 * original location).
 *
 *  Created on: October 26, 2021
 *      Author: Sean LaPlante
 */
import processing.sound.*;

SoundFile soundFile = null;
String soundFilePath = null;
String pbFilePath = null;
boolean setupComplete = false;
int resolutionX = 0;
int resolutionY = 0;
int drawIdx = 0;
ArrayList<PlaybackItem> pbItems = new ArrayList<PlaybackItem>();


void fileSelected(File selection) {
    if (selection == null) {
        println("Window was closed or the user hit cancel.");
    } else {
        pbFilePath = selection.getAbsolutePath();
        println("User selected " + pbFilePath);
    }
}


void parseFile(String filepath) {
    BufferedReader reader = createReader(filepath);
    String line = null;
    int index = -1;
      
    try {
        while ((line = reader.readLine()) != null) {
            index++;
            
            if (index == 0) {
                // First item is the full path to the song file
                soundFilePath = line;
                continue;
            }
      
            // All items begin with an x and y
            String[] pieces = split(line, ",");
            int x = int(pieces[0]);
            int y = int(pieces[1]);
      
            if (index == 1) {
                // but, the second item is just the image resolution. So just x,y
                resolutionX = x;
                resolutionY = y;
                continue;
            }
      
            int r = int(pieces[2]);
            int g = int(pieces[3]);
            int b = int(pieces[4]);
            int a = int(pieces[5]);
            float timestamp = float(pieces[6]);
                       
            pbItems.add(new PlaybackItem(x, y, r, g, b, a, timestamp));
        }
        reader.close();
    } catch (IOException e) {
        e.printStackTrace();
    }
} 

void setup() {
    size(600, 600);
    frameRate(90);
    selectInput("Select a *.pb file to process:", "fileSelected");
}


void draw() {
    if (pbFilePath != null && !setupComplete) {
        println("Parsing: " + pbFilePath);
        parseFile(pbFilePath);            
        if (soundFilePath == null) {
            exit();
        }
        println("Image Resolution: " + resolutionX + "x" + resolutionY);
        println("Playing: " + soundFilePath);
        
        // Resize the window
        surface.setTitle(soundFilePath);
        surface.setResizable(true);
        surface.setSize(resolutionX, resolutionY);
        surface.setResizable(false);
             
        // Load and play the song
        soundFile = new SoundFile(this, soundFilePath);
        if (soundFile == null) {
            println("unable to play " + soundFilePath);
            exit();
        }
        soundFile.play();
        setupComplete = true;
    }
    
    if (!setupComplete || !soundFile.isPlaying()) {
        return;
    }
    
    float songPos = soundFile.position();
    int count = 0;
    PlaybackItem item = pbItems.get(0);
    while(pbItems.size() > 0 && item.should_pop(songPos)) {
        item = pbItems.get(0);
        item.display();
        pbItems.remove(0);
        count++;
    }
    if (count >= 1000) {
        println("TOO MUCH DATA. Drawing is likely to fall behind.");
    }
}
