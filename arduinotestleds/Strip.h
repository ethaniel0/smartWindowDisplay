#ifndef STRIP_H
#define STRIP_H
 
#include <Arduino.h>
#include <FastLED.h>

class Strip {
public:
      Strip(CRGB* leds, int numLights);
      ~Strip();
      void set(int led, CRGB color);
      void set(CRGB* colors, int start);
      void setBright(int led, int val);
      
      CRGB get(int led);
      CRGB* getStrip();

      CRGB randColor();
      CRGB randColor(int minim, int maxim);
      CRGB randColor(int rmin, int rmax, int gmin, int gmax, int bmin, int bmax);

      void blank();
      void blank(int from);
      void blank(int from, int to);                                                              // verified

      void fill(CRGB color);
      void fill(CRGB color, int from);
      void fill(CRGB color, int from, int to);                                                   // verified

      void fillBright(int val);
      void fillBright(int val, int from);
      void fillBright(int val, int from, int to);                                                // verified

      void fillBrightRand(int low, int high);
      void fillBrightRand(int low, int high, int from);
      void fillBrightRand(int low, int high, int from, int to);                                  // verified

      void fillHSVRand(CHSV color, int h);
      void fillHSVRand(CHSV color, int h, int s);
      void fillHSVRand(CHSV color, int h, int s, int v);
      void fillHSVRand(CHSV color, int h, int s, int v, int from);
      void fillHSVRand(CHSV color, int h, int s, int v, int from, int to);                        // verified

      void fillRGBRand(CRGB color, int r);
      void fillRGBRand(CRGB color, int r, int g);
      void fillRGBRand(CRGB color, int r, int g, int b);
      void fillRGBRand(CRGB color, int r, int g, int b, int from);
      void fillRGBRand(CRGB color, int r, int g, int b, int from, int to);                         // verified
      
      // shifts down
      CRGB shift();
      CRGB shift(CRGB color);
      CRGB shift(int from, int to);
      CRGB shift(CRGB color, int from, int to);                                                    // verified
      
      // shifts up
      CRGB unshift();
      CRGB unshift(CRGB color);
      CRGB unshift(int from, int to);
      CRGB unshift(CRGB color, int from, int to);                                                   // verified

      void flip();
      void flip(int from);
      void flip(int from, int to);                                                                   // verified

      void gradient(CRGB color1, CRGB color2);
      void gradient(CRGB color1, CRGB color2, int from);
      void gradient(CRGB color1, CRGB color2, int from, int to);                                     // verified

      void gradientHSVRand(CHSV color1, CHSV color2, int h);
      void gradientHSVRand(CHSV color1, CHSV color2, int h, int s);
      void gradientHSVRand(CHSV color1, CHSV color2, int h, int s, int v);
      void gradientHSVRand(CHSV color1, CHSV color2, int h, int s, int v, int from);
      void gradientHSVRand(CHSV color1, CHSV color2, int h, int s, int v, int from, int to);          // verified

      void gradientRGBRand(CRGB color1, CRGB color2, int r);
      void gradientRGBRand(CRGB color1, CRGB color2, int r, int g);
      void gradientRGBRand(CRGB color1, CRGB color2, int r, int g, int b);
      void gradientRGBRand(CRGB color1, CRGB color2, int r, int g, int b, int from);
      void gradientRGBRand(CRGB color1, CRGB color2, int r, int g, int b, int from, int to);           // verified

      void gradientBrightRand(CRGB color1, CRGB color2);
      void gradientBrightRand(CRGB color1, CRGB color2, int low);
      void gradientBrightRand(CRGB color1, CRGB color2, int low, int high);
      void gradientBrightRand(CRGB color1, CRGB color2, int low, int high, int from);
      void gradientBrightRand(CRGB color1, CRGB color2, int low, int high, int from, int to);          // verified

      void snapToGradient(CRGB color1, CRGB color2, int from, int to);

      
private:
      int lights;
      CRGB* strip;
};

#endif
