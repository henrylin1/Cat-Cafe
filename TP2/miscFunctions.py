def blBlit(surface, image, loc):
    rect = image.get_rect
    topleft = (loc[0] - rect.bottomleft[0], loc[1] - rect.bottomleft[1])
    surface.blit(image,topleft)
    return surface