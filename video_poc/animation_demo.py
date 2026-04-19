from moviepy.editor import TextClip, CompositeVideoClip

txt = TextClip(
    "Hello Python Animation",
    fontsize=70,
    color='white',
    size=(800,400)
).set_duration(5)

txt = txt.set_position(('center','center'))

video = CompositeVideoClip([txt], size=(1280,720))
video.write_videofile("animation.mp4", fps=24)