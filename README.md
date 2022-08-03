# Face Recognition Attendence Application

When you clone/download this project, you get one simple command-line program:
`FaceRecognizer` - Recognize faces in a folder full for **known people** photographs, in which `HumanResourceSystem` is implemented to track attendence for each employee added in to the system.

First, you need to provide a folder with pictures of each known person. There should be **at least one image file for each person** with the files named according who he/she is, followed by a **optional** index (if two or more images of a person is provided) with a seperator of **"_"**. Image files should be named like, for example, Joe Biden_1, Joe Biden_2  

![known](https://cloud.githubusercontent.com/assets/896692/23582466/8324810e-00df-11e7-82cf-41515eba704d.png)

```python
from face_recognizer import FaceRecognizer
# is_headless param will control whether the program will run in the background or not.
recognizer = FaceRecognizer(
    images_folder_path = "./known_people", 
    is_headless= False
)
# the code below will start a video capturer to dectect known people's face, 
# thus to collect the timestamp information based on when he/she is detected
# for breaking the video capturer, pressing "q" as exit key.
recognizer.run()

```

After breaking .run() method, it will returns a DataFrame containing attendence information **(e.g., employee name, date, start working time, end working time, total working hours)** stored in `HumanResourceSystem`, and automatically output a csv file (named based on date when the program is executed, e.g. `20220101.csv`, if timestamps (i.e., date) collected across more than **1 day**, file name may be named, for example, `20220101-20220102.csv`)

For accessing timestamp information (as DataFrame) maybe for further data processing, try running the code below, which will yield a DataFrame.

```python
recognizer.human_resources_system.output_current_seession_punchcard_info()
```

<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>name</th>      <th>date</th>      <th>on_work</th>      <th>off_work</th>      <th>working_hour</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>William</td>      <td>2022-08-03</td>      <td>01:36:50</td>      <td>01:37:00</td>      <td>00:00:10</td>    </tr>  </tbody></table>
