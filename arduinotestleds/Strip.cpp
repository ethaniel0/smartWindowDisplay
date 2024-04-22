#include <Arduino.h>
#include <FastLED.h>
#include "Strip.h"

Strip::Strip(CRGB* leds, int numLights){
  strip = leds;
  lights = numLights;
}

Strip::~Strip(){}

void Strip::set(int led, CRGB color){ strip[led] = color; }
void Strip::set(CRGB* colors, int start){ 
  int len = sizeof(colors) / sizeof(colors[0]);
  for (int i = start; i < start + len && i < lights; i++) strip[i] = colors[i-start];
}

void Strip::setBright(int led, int val){ strip[led] %= val; }

CRGB Strip::get(int led){ return strip[led]; }
CRGB* Strip::getStrip(){ return strip; }

CRGB Strip::randColor(){ return CRGB(random(0, 255), random(0, 255), random(0, 255)); }
CRGB Strip::randColor(int minim, int maxim){ return CRGB(random(minim, maxim), random(minim, maxim), random(minim, maxim)); }
CRGB Strip::randColor(int rmin, int rmax, int gmin, int gmax, int bmin, int bmax){ return CRGB(random(rmin, rmax), random(gmin, gmax), random(bmin, bmax)); }


void Strip::blank(){ for (int i = 0; i < lights; i++) set(i, CRGB(0, 0, 0)); }
void Strip::blank(int from){ blank(from, lights); }
void Strip::blank(int from, int to){ for (int i = from; i < to; i++) set(i, CRGB(0, 0, 0)); }

void Strip::fill(CRGB color){ fill(color, 0, lights); }
void Strip::fill(CRGB color, int from){ fill(color, from, lights); }
void Strip::fill(CRGB color, int from, int to){ for (int i = from; i < to; i++) set(i, color); }

void Strip::fillBright(int val){ fillBright(val, 0, lights); }
void Strip::fillBright(int val, int from){ fillBright(val, from, lights); }
void Strip::fillBright(int val, int from, int to){ for (int i = from; i < to; i++) setBright(i, val); }

void Strip::fillBrightRand(int low, int high){ fillBrightRand(low, high, 0, lights); }
void Strip::fillBrightRand(int low, int high, int from){ fillBrightRand(low, high, from, lights); }
void Strip::fillBrightRand(int low, int high, int from, int to){
  for (int i = from; i < to; i++){
      setBright(i, random(low, high+1)); 
  } 
}

void Strip::fillHSVRand(CHSV color, int h){ fillHSVRand(color, h, 0, 0, 0, lights); }
void Strip::fillHSVRand(CHSV color, int h, int s){ fillHSVRand(color, h, s, 0, 0, lights); }
void Strip::fillHSVRand(CHSV color, int h, int s, int v){ fillHSVRand(color, h, s, v, 0, lights); }
void Strip::fillHSVRand(CHSV color, int h, int s, int v, int from){ fillHSVRand(color, h, s, v, from, lights);}
void Strip::fillHSVRand(CHSV color, int h, int s, int v, int from, int to){
  for (int i = from; i < to; i++){
    int hvar = color.hue + random(-h, h+1);
    int svar = color.sat + random(-s, s+1);
    int vvar = color.val + random(-v, v+1);
    set(i, CHSV(hvar % 256, svar % 256, vvar % 256)); 
  } 
}

void Strip::fillRGBRand(CRGB color, int r){fillRGBRand(color, r, 0, 0, 0, lights); }
void Strip::fillRGBRand(CRGB color, int r, int g){fillRGBRand(color, r, g, 0, 0, lights); }
void Strip::fillRGBRand(CRGB color, int r, int g, int b){fillRGBRand(color, r, g, b, 0, lights); }
void Strip::fillRGBRand(CRGB color, int r, int g, int b, int from){fillRGBRand(color, r, g, b, from, lights); }
void Strip::fillRGBRand(CRGB color, int r, int g, int b, int from, int to){
  if (to == -1) to = lights;
  for (int i = from; i < to; i++){
    int rvar = color[0] + random(-r, r+1);
    int gvar = color[1] + random(-g, g+1);
    int bvar = color[2] + random(-b, b+1);
    set(i, CRGB(min(rvar, 255), min(gvar, 255), min(bvar, 255)));
  }
}


CRGB Strip::shift(){ return shift(CRGB(0, 0, 0), 0, lights); }
CRGB Strip::shift(CRGB color){ return shift(color, 0, lights); }
CRGB Strip::shift(int from, int to){ return shift(CRGB(0, 0, 0), from, to); }
CRGB Strip::shift(CRGB color, int from, int to){
  CRGB last = strip[to-1];
  for (int i = to - 1; i > from; i--) set(i, strip[i-1]);
  set(from, color);
  return last;
}

CRGB Strip::unshift(){ return unshift(CRGB(0, 0, 0), 0, lights); }
CRGB Strip::unshift(CRGB color){ return unshift(color, 0, lights); }
CRGB Strip::unshift(int from, int to){ return unshift(CRGB(0, 0, 0), from, to); }
CRGB Strip::unshift(CRGB color, int from, int to){
  CRGB first = strip[0];
  for (int i = from; i < to - 1; i++) set(i, strip[i+1]);
  set(to - 1, color);
  return first;
}

void Strip::flip(){ flip(0, lights); }
void Strip::flip(int from){ flip(from, lights); };
void Strip::flip(int from, int to){
  int dist = to - from;
  for (int i = 0; i <  dist/2; i++){
    CRGB temp = strip[from + i];
    set(from+i, strip[to - 1 - i]);
    set(to-1-i, temp);
  }
}

void Strip::gradient(CRGB color1, CRGB color2){gradient(color1, color2, 0, lights);}
void Strip::gradient(CRGB color1, CRGB color2, int from){gradient(color1, color2, from, lights);}
void Strip::gradient(CRGB c1, CRGB c2, int from, int to){
  int dist = to - from;
  for (int i = from; i < to; i++){
    int d = i-from;
    int r = c1[0] * (dist-d)/dist + c2[0] * d/dist;
    int g = c1[1] * (dist-d)/dist + c2[1] * d/dist;
    int b = c1[2] * (dist-d)/dist + c2[2] * d/dist;

    set(i, CRGB(r, g, b));
  }
  
}

void Strip::gradientHSVRand(CHSV c1, CHSV c2, int h){ gradientHSVRand(c1, c2, h, 0, 0, 0, lights); }
void Strip::gradientHSVRand(CHSV c1, CHSV c2, int h, int s){ gradientHSVRand(c1, c2, h, s, 0, 0, lights); }
void Strip::gradientHSVRand(CHSV c1, CHSV c2, int h, int s, int v){ gradientHSVRand(c1, c2, h, s, v, 0, lights); }
void Strip::gradientHSVRand(CHSV c1, CHSV c2, int h, int s, int v, int from){ gradientHSVRand(c1, c2, h, s, v, from, lights); }
void Strip::gradientHSVRand(CHSV c1, CHSV c2, int hv, int sv, int vv, int from, int to){
  int dist = to - from;
  for (int i = from; i < to && i < lights; i++){
    int d = i-from;
    
    int hvar = random(-hv, hv+1);
    int svar = random(-sv, sv+1);
    int vvar = random(-vv, vv+1);
    
    int h = c1.hue * (dist-d)/dist + c2.hue * d/dist;
    int s = c1.sat * (dist-d)/dist + c2.sat * d/dist;
    int v = c1.val * (dist-d)/dist + c2.val * d/dist;

    
    set(i, CHSV((h+hvar)%256, min(255, max(0, s+svar)), min(255, max(0, v+vvar))));
  }
}

void Strip::gradientRGBRand(CRGB c1, CRGB c2, int r){ gradientRGBRand(c1, c2, r, 0, 0, 0, lights); }
void Strip::gradientRGBRand(CRGB c1, CRGB c2, int r, int g){ gradientRGBRand(c1, c2, r, g, 0, 0, lights); }
void Strip::gradientRGBRand(CRGB c1, CRGB c2, int r, int g, int b){ gradientRGBRand(c1, c2, r, g, b, 0, lights); }
void Strip::gradientRGBRand(CRGB c1, CRGB c2, int r, int g, int b, int from){ gradientRGBRand(c1, c2, r, g, b, from, lights); }
void Strip::gradientRGBRand(CRGB c1, CRGB c2, int rv, int gv, int bv, int from, int to){
  int dist = to - from;
  for (int i = from; i < to; i++){
    int d = i-from;

    int rvar = random(-rv, rv+1);
    int gvar = random(-gv, gv+1);
    int bvar = random(-bv, bv+1);

    int r = c1[0] * (dist-d)/dist + c2[0] * d/dist;
    int g = c1[1] * (dist-d)/dist + c2[1] * d/dist;
    int b = c1[2] * (dist-d)/dist + c2[2] * d/dist;

    CRGB c = CRGB(r, g, b) + CRGB(rvar, gvar, bvar);
    c |= 0;
    c &= 255;

    set(i, c);
  }
}

void Strip::gradientBrightRand(CRGB c1, CRGB c2){ gradientBrightRand(c1, c2, 0, 100, 0, lights); }
void Strip::gradientBrightRand(CRGB c1, CRGB c2, int low){ gradientBrightRand(c1, c2, low, 100, 0, lights); }
void Strip::gradientBrightRand(CRGB c1, CRGB c2, int low, int high){ gradientBrightRand(c1, c2, low, high, 0, lights); }
void Strip::gradientBrightRand(CRGB c1, CRGB c2, int low, int high, int from){ gradientBrightRand(c1, c2, low, high, from, lights); }
void Strip::gradientBrightRand(CRGB c1, CRGB c2, int low, int high, int from, int to){
  gradient(c1, c2, from, to);
  fillBrightRand(low, high, from, to); 
}

void Strip::snapToGradient(CRGB c1, CRGB c2, int from, int to){
  int dist = to - from;
  for (int i = from; i < to; i++){
    if(strip[i] != CRGB(0, 0, 0)){
      int d = i-from;
      int r = c1[0] * (dist-d)/dist + c2[0] * d/dist;
      int g = c1[1] * (dist-d)/dist + c2[1] * d/dist;
      int b = c1[2] * (dist-d)/dist + c2[2] * d/dist;
      set(i, CRGB(r, g, b));
    }
  }
}
