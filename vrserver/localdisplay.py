
import pygame

from vrserver.sensorlistener import SensorListener


class LocalDisplay(SensorListener):
    def __init__(self):
        super(LocalDisplay, self).__init__()
        pygame.init()
        pygame.font.init()
        self._display = pygame.display.set_mode(
            (800, 600),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

    def on_gnss_event(self, gnss_event):
        # print('gnss_event:', str(gnss_event))
        pass

    def on_camera_rgb_event(self, image):
        print('on_camera_rgb_event:', image['image'].shape)
        #cv2.imshow('SensorListener', image['image'])
        # cv2.waitKey()
        array = image['image']
        array = array[:, :, ::-1]
        array = array.swapaxes(0, 1)
        self._display.blit(pygame.surfarray.make_surface(array), (0, 0))
        pygame.display.flip()
