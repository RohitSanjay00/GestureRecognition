import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import threading 
import os

class Handlandmarks:
    #gesture = []
    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
    VisionRunningMode = mp.tasks.vision.RunningMode
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    handpoints = mp.tasks.vision.HandLandmarkerResult
    
    
    def __init__(self, keypoints,  frame, timestamp):
        self.frame = frame
        self.timestamp = timestamp
        self.keypoints = keypoints
        
    

    def get_landmarks(self):
        options = self.HandLandmarkerOptions(
                base_options=self.BaseOptions(model_asset_path='hand_landmarker.task'),
                running_mode=self.VisionRunningMode.LIVE_STREAM,
                result_callback=self.__result_callback)
        with self.HandLandmarker.create_from_options(options) as landmarker:
            np_array = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np_array )
            landmarker.detect_async(mp_image, self.timestamp)
    
    
    def __result_callback(self, result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.handpoints = result
        if len(result.hand_world_landmarks) == 0 : 
            for i in range(21):
                landmark_values = np.array([0.0, 0.0, 0.0])
                self.keypoints.append(landmark_values)
        else:
            hand_landmarks_list = result.hand_world_landmarks
            for idx in range(len(hand_landmarks_list)):
                hand_landmarks = hand_landmarks_list[idx]
                for landmarks in hand_landmarks:
                    #print("x:",landmarks.x)
                    #print("y:",landmarks.y)
                    #print("z:",landmarks.z)
                    landmark_values = np.array([landmarks.x,landmarks.y, landmarks.z])
                    self.keypoints.append(landmark_values)

    def returngesture(self):
        #self.keypoints = self.
        return self.keypoints
    
    def returnhandmarks(self):
        return self.handpoints
    
    def markings(self, frame, detection_result):
        hand_landmarks_list = detection_result.hand_landmarks
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
            solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style())
        return frame
    
