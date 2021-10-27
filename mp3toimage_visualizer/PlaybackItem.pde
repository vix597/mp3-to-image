/*
 * PlaybackItem.pde
 *
 * Java version of the class with the same name
 * from the Python code to represent one row
 * in the .pb CSV file.
 *
 *  Created on: October 26, 2021
 *      Author: Sean LaPlante
 */

class PlaybackItem {
    /*
     * An item to playback. Has position, color, time, etc.
     */
    private int positionX;
    private int positionY;
    private color c;
    private float timestamp;

    PlaybackItem(int x, int y, int r, int g, int b, int a, float ts) {
        positionX = x;
        positionY = y;
        c = color(r, g, b, a);
        timestamp = ts;
    }

    boolean should_pop(float ts) {
        /*
         * Given the provided timestamp, should this item be removed from the
         * list of items?
         */
        return ts >= timestamp;
    }

    void display() {
        stroke(c);
        point(positionX, positionY);
    }
}
