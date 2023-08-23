
existingSprites = []

import Modules.Core.NewColliderManager as NewColliderManager
import pygame
import math
class Sprite:
    def __init__(self,Properties):
        self.JumpBoost = Properties["JumpBoost"] if Properties.get("JumpBoost") else 0
        self.Type = Properties["Type"]
        self.Static = Properties["Static"] if Properties.get("Static") else False
        self.Scale = Properties["Scale"] if Properties.get("Scale") else 1
        self.Texture = pygame.image.load("local/Assets/Sprites/"  + self.Type + ".png")
        self.Rotation = Properties["Rotation"] if Properties.get("Rotation") else 0
        self.FittedTexture  = self.GetFittedTexture()     
        self.Collider =  NewColliderManager.new(Properties)
        existingSprites.append(self)      
        
    def GetFittedTexture(self):
        x = self.Scale
        
        ScaledTexture = pygame.transform.scale(self.Texture, (50 * x,50 * x))
        ScaledTexture = pygame.transform.rotate(ScaledTexture,90*self.Rotation)
        return ScaledTexture    
        
def CheckRendering():
    global existingSprites
    for Sprite in existingSprites:    
        ObjectWidth = Sprite.Collider.Width
        if Sprite.Collider.Location[0] < -ObjectWidth:
            existingSprites.remove(Sprite)

class JumpOrb(Sprite):
    def __init__(self, Properties):     
        Properties["Height"] = 35
        Properties["Width"] = 35 
        Properties["Scale"] = 0.8
        Properties["Tags"] = [Properties["OrbType"]]
        Properties["Type"] = Properties["Tags"][0] + "Orb"
        Properties["Tags"].append("JumpOrb") 
        Properties["Trigger"] = True
        super().__init__(Properties)
        
class Spike(Sprite):
    def __init__(self,Properties):
        Properties["Type"] = "Spike"
        Properties["Tags"] = ["KillObject"]
        Rotation = Properties["Rotation"] if Properties.get("Rotation") else 0
        Cos = math.cos(math.radians(Rotation * 90))
        Sin = math.sin(math.radians(Rotation * 90))
        Properties["Width"] = abs(20 * Cos) + abs(40 * Sin)
        Properties["Height"] = abs(20 * Sin) + abs(40 * Cos)
        xDeviation,yDeviation = CalculateDeviation(Rotation)
        Properties["Location"][0] += xDeviation
        Properties["Location"][1] += yDeviation
        super().__init__(Properties)

class Saw(Sprite):
    def __init__(self,Properties):
        Properties["Type"] = "Saw"
        Properties["Tags"] = ["KillObject"]
        Properties["Width"] = 75
        Properties["Height"] = 75
        Properties["Scale"] = 2
        super().__init__(Properties)

class Block(Sprite):
    def __init__(self, Properties):
        Properties["Width"] *= 50
        Properties["Height"] *= 50
        super().__init__(Properties)

class JumpPad(Sprite):
    def __init__(self, Properties):
        Rotation = Properties["Rotation"] if Properties.get("Rotation") else 0
        Cos = math.cos(math.radians(Rotation * 90))
        Sin = math.sin(math.radians(Rotation * 90))
        Properties["Width"] = abs(50 * Cos) + abs(20 * Sin)
        Properties["Height"] = abs(50 * Sin) + abs(20 * Cos)
        Properties["Tags"] = [Properties["PadType"]]
        Properties["Type"] = Properties["Tags"][0] + "Pad"
        Properties["Tags"].append("JumpPad") 
        Properties["Location"][1] += 30
        Properties["Trigger"] = True
        super().__init__(Properties)

def Clear():
    global existingSprites
    existingSprites = []


def new(Properties):
    if Properties.get("Object") == "Block":
        return Block(Properties)
    elif Properties.get("Object") == "JumpOrb":
        return JumpOrb(Properties)
    elif Properties.get("Object") == "Spike":
        return Spike(Properties)
    elif Properties.get("Object") == "Saw":
        return Saw(Properties)
    elif Properties.get("Object") == "JumpPad":
        return JumpPad(Properties)
    
def FrameStepped(screen):
    for Sprite in existingSprites:
        if Sprite.Type == "Block":
            DrawBlock(screen, Sprite.Collider.Height, Sprite.Collider.Width, Sprite.Collider.Location, Sprite.FittedTexture)
        elif Sprite.Type == "Spike":
            xDeviation,yDeviation = CalculateDeviation(Sprite.Rotation)
            screen.blit(Sprite.FittedTexture, (Sprite.Collider.Location[0] -xDeviation,Sprite.Collider.Location[1] - yDeviation))

        elif Sprite.Type == "Saw":
            ColliderSize = [Sprite.Collider.Height, Sprite.Collider.Width]
            ScaleDifference = ColliderSize[0]/2

            Texture = pygame.transform.rotate(Sprite.FittedTexture, Sprite.Rotation)
            ColliderRect = Texture.get_rect()
            ColliderRect.center = (Sprite.Collider.Location[0] + ScaleDifference, Sprite.Collider.Location[1] + ScaleDifference)

            screen.blit(Texture, ColliderRect)
            Sprite.Rotation -= 2
        elif Sprite.Type.count("Pad") > 0:
            screen.blit(Sprite.FittedTexture, (Sprite.Collider.Location[0] ,Sprite.Collider.Location[1] -30 ))
        else:   
            Size = Sprite.FittedTexture.get_size()
            Pos = Sprite.Collider.Location
            Rect = pygame.Rect(Pos, Size)
            Rect.center = (Pos[0] + Size[0]/2.2, Pos[1] + Size[1]/2.2)
            screen.blit(Sprite.FittedTexture, Rect)


def CalculateDeviation(Rotation):
    xDeviation = 0
    yDeviation = 0
    if Rotation == 1 or Rotation == 3:
        yDeviation = 15
        xDeviation = 10 if Rotation == 1 else 0
    else: 
        xDeviation = 15
        yDeviation = 10 if Rotation == 4 or Rotation == 0 else 0
    return xDeviation,yDeviation

def DrawBlock(Screen, Height, Width,Location, FittedTexture):
    for y in range(int(Height)//50): 
        for x in range(int(Width)//50):       
            Screen.blit(FittedTexture, (x*50 + Location[0], y*50 + Location[1]))