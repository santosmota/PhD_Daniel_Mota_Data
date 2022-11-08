Ts = 0.005
time_to_samples = 1.0 / Ts

dict_slider_marks = {}
for t in range(0, 200, 5):
    dict_slider_marks[int(t*time_to_samples)] = str(t)