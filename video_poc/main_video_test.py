import cv2
import numpy as np

width, height = 640, 360
fps = 24
duration = 5
total_frames = fps * duration

# Use XVID codec and .avi
out = cv2.VideoWriter('output_video.avi',
                      cv2.VideoWriter_fourcc(*'XVID'),
                      fps,
                      (width, height))

for i in range(total_frames):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(frame, "Hello OpenCV!", (50, height//2),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    out.write(frame)

out.release()
print("Video created successfully!")