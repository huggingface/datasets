---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- image-classification
task_ids:
- multi-class-image-classification
paperswithcode_id: quick-draw-dataset
pretty_name: Quick, Draw!
---

# Dataset Card for Quick, Draw!

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [Quick, Draw! homepage](https://quickdraw.withgoogle.com/data)
- **Repository:** [Quick, Draw! repository](https://github.com/googlecreativelab/quickdraw-dataset)
- **Paper:** [A Neural Representation of Sketch Drawings](https://arxiv.org/abs/1704.03477v4)
- **Leaderboard:** [Quick, Draw! Doodle Recognition Challenge](https://www.kaggle.com/competitions/quickdraw-doodle-recognition/leaderboard)
- **Point of Contact:** [Quick, Draw! support](mailto:quickdraw-support@google.com)

### Dataset Summary

The Quick Draw Dataset is a collection of 50 million drawings across 345 categories, contributed by players of the game Quick, Draw!. The drawings were captured as timestamped vectors, tagged with metadata including what the player was asked to draw and in which country the player was located.

### Supported Tasks and Leaderboards

- `image-classification`: The goal of this task is to classify a given sketch into one of 345 classes.
The (closed) leaderboard for this task is available [here](https://www.kaggle.com/competitions/quickdraw-doodle-recognition/leaderboard).

### Languages

English.

## Dataset Structure

### Data Instances

#### `raw`

A data point comprises a drawing and its metadata.

```
{
  'key_id': '5475678961008640',
  'word': 0,
  'recognized': True,
  'timestamp': datetime.datetime(2017, 3, 28, 13, 28, 0, 851730),
  'countrycode': 'MY',
  'drawing': {
    'x': [[379.0, 380.0, 381.0, 381.0, 381.0, 381.0, 382.0], [362.0, 368.0, 375.0, 380.0, 388.0, 393.0, 399.0, 404.0, 409.0, 410.0, 410.0, 405.0, 397.0, 392.0, 384.0, 377.0, 370.0, 363.0, 356.0, 348.0, 342.0, 336.0, 333.0], ..., [477.0, 473.0, 471.0, 469.0, 468.0, 466.0, 464.0, 462.0, 461.0, 469.0, 475.0, 483.0, 491.0, 499.0, 510.0, 521.0, 531.0, 540.0, 548.0, 558.0, 566.0, 576.0, 583.0, 590.0, 595.0, 598.0, 597.0, 596.0, 594.0, 592.0, 590.0, 589.0, 588.0, 586.0]],
    'y': [[1.0, 7.0, 15.0, 21.0, 27.0, 32.0, 32.0], [17.0, 17.0, 17.0, 17.0, 16.0, 16.0, 16.0, 16.0, 18.0, 23.0, 29.0, 32.0, 32.0, 32.0, 29.0, 27.0, 25.0, 23.0, 21.0, 19.0, 17.0, 16.0, 14.0], ..., [151.0, 146.0, 139.0, 131.0, 125.0, 119.0, 113.0, 107.0, 102.0, 99.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 98.0, 100.0, 102.0, 104.0, 105.0, 110.0, 115.0, 121.0, 126.0, 131.0, 137.0, 142.0, 148.0, 150.0]],
    't': [[0, 84, 100, 116, 132, 148, 260], [573, 636, 652, 660, 676, 684, 701, 724, 796, 838, 860, 956, 973, 979, 989, 995, 1005, 1012, 1020, 1028, 1036, 1053, 1118], ..., [8349, 8446, 8468, 8484, 8500, 8516, 8541, 8557, 8573, 8685, 8693, 8702, 8710, 8718, 8724, 8732, 8741, 8748, 8757, 8764, 8773, 8780, 8788, 8797, 8804, 8965, 8996, 9029, 9045, 9061, 9076, 9092, 9109, 9167]]
  }
}
```

#### `preprocessed_simplified_drawings`

The simplified version of the dataset generated from the `raw` data with the simplified vectors, removed timing information, and the data positioned and scaled into a 256x256 region.
The simplification process was:
    1.Align the drawing to the top-left corner, to have minimum values of 0.
    2.Uniformly scale the drawing, to have a maximum value of 255.
    3.Resample all strokes with a 1 pixel spacing.
    4.Simplify all strokes using the [Ramer-Douglas-Peucker algorithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm) with an epsilon value of 2.0.

```
{
  'key_id': '5475678961008640',
  'word': 0,
  'recognized': True,
  'timestamp': datetime.datetime(2017, 3, 28, 15, 28),
  'countrycode': 'MY',
  'drawing': {
    'x': [[31, 32], [27, 37, 38, 35, 21], [25, 28, 38, 39], [33, 34, 32], [5, 188, 254, 251, 241, 185, 45, 9, 0], [35, 35, 43, 125, 126], [35, 76, 80, 77], [53, 50, 54, 80, 78]],
    'y': [[0, 7], [4, 4, 6, 7, 3], [5, 10, 10, 7], [4, 33, 44], [50, 50, 54, 83, 86, 90, 86, 77, 52], [85, 91, 92, 96, 90], [35, 37, 41, 47], [34, 23, 22, 23, 34]]
  }
}
```

#### `preprocessed_bitmaps` (default configuration)

This configuration contains the 28x28 grayscale bitmap images that were generated from the simplified data, but are aligned to the center of the drawing's bounding box rather than the top-left corner. The code that was used for generation is available [here](https://github.com/googlecreativelab/quickdraw-dataset/issues/19#issuecomment-402247262).

```
{
  'image': <PIL.PngImagePlugin.PngImageFile image mode=L size=28x28 at 0x10B5B102828>,
  'label': 0
}
```

#### `sketch_rnn` and `sketch_rnn_full`

The `sketch_rnn_full` configuration stores the data in the format suitable for inputs into a recurrent neural network and was used for for training the [Sketch-RNN](https://arxiv.org/abs/1704.03477) model. Unlike `sketch_rnn` where the samples have been randomly selected from each category, the `sketch_rnn_full` configuration contains the full data for each category.

```
{
  'word': 0,
  'drawing': [[132, 0, 0], [23, 4, 0], [61, 1, 0], [76, 0, 0], [22, -4, 0], [152, 0, 0], [50, -5, 0], [36, -10, 0], [8, 26, 0], [0, 69, 0], [-2, 11, 0], [-8, 10, 0], [-56, 24, 0], [-23, 14, 0], [-99, 40, 0], [-45, 6, 0], [-21, 6, 0], [-170, 2, 0], [-81, 0, 0], [-29, -9, 0], [-94, -19, 0], [-48, -24, 0], [-6, -16, 0], [2, -36, 0], [7, -29, 0], [23, -45, 0], [13, -6, 0], [41, -8, 0], [42, -2, 1], [392, 38, 0], [2, 19, 0], [11, 33, 0], [13, 0, 0], [24, -9, 0], [26, -27, 0], [0, -14, 0], [-8, -10, 0], [-18, -5, 0], [-14, 1, 0], [-23, 4, 0], [-21, 12, 1], [-152, 18, 0], [10, 46, 0], [26, 6, 0], [38, 0, 0], [31, -2, 0], [7, -2, 0], [4, -6, 0], [-10, -21, 0], [-2, -33, 0], [-6, -11, 0], [-46, 1, 0], [-39, 18, 0], [-19, 4, 1], [-122, 0, 0], [-2, 38, 0], [4, 16, 0], [6, 4, 0], [78, 0, 0], [4, -8, 0], [-8, -36, 0], [0, -22, 0], [-6, -2, 0], [-32, 14, 0], [-58, 13, 1], [-96, -12, 0], [-10, 27, 0], [2, 32, 0], [102, 0, 0], [1, -7, 0], [-27, -17, 0], [-4, -6, 0], [-1, -34, 0], [-64, 8, 1], [129, -138, 0], [-108, 0, 0], [-8, 12, 0], [-1, 15, 0], [12, 15, 0], [20, 5, 0], [61, -3, 0], [24, 6, 0], [19, 0, 0], [5, -4, 0], [2, 14, 1]]
}
```

### Data Fields

#### `raw`

- `key_id`: A unique identifier across all drawings.
- `word`: Category the player was prompted to draw.
- `recognized`: Whether the word was recognized by the game.
- `timestamp`: When the drawing was created.
- `countrycode`: A two letter country code ([ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) of where the player was located.
- `drawing`: A dictionary where `x` and `y` are the pixel coordinates, and `t` is the time in milliseconds since the first point. `x` and `y` are real-valued while `t` is an integer. `x`, `y` and `t` match in lenght and are represented as lists of lists where each sublist corresponds to a single stroke. The raw drawings can have vastly different bounding boxes and number of points due to the different devices used for display and input.

#### `preprocessed_simplified_drawings`

- `key_id`: A unique identifier across all drawings.
- `word`: Category the player was prompted to draw.
- `recognized`: Whether the word was recognized by the game.
- `timestamp`: When the drawing was created.
- `countrycode`: A two letter country code ([ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) of where the player was located.
- `drawing`: A simplified drawing represented as a dictionary where `x` and `y` are the pixel coordinates. The simplification processed is described in the `Data Instances` section.

#### `preprocessed_bitmaps` (default configuration)

- `image`: A `PIL.Image.Image` object containing the 28x28 grayscale bitmap. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `label`: Category the player was prompted to draw.

<details>
  <summary>
  Click here to see the full class labels mapping:
  </summary>

  |id|class|
  |---|---|
  |0|aircraft carrier|
  |1|airplane|
  |2|alarm clock|
  |3|ambulance|
  |4|angel|
  |5|animal migration|
  |6|ant|
  |7|anvil|
  |8|apple|
  |9|arm|
  |10|asparagus|
  |11|axe|
  |12|backpack|
  |13|banana|
  |14|bandage|
  |15|barn|
  |16|baseball bat|
  |17|baseball|
  |18|basket|
  |19|basketball|
  |20|bat|
  |21|bathtub|
  |22|beach|
  |23|bear|
  |24|beard|
  |25|bed|
  |26|bee|
  |27|belt|
  |28|bench|
  |29|bicycle|
  |30|binoculars|
  |31|bird|
  |32|birthday cake|
  |33|blackberry|
  |34|blueberry|
  |35|book|
  |36|boomerang|
  |37|bottlecap|
  |38|bowtie|
  |39|bracelet|
  |40|brain|
  |41|bread|
  |42|bridge|
  |43|broccoli|
  |44|broom|
  |45|bucket|
  |46|bulldozer|
  |47|bus|
  |48|bush|
  |49|butterfly|
  |50|cactus|
  |51|cake|
  |52|calculator|
  |53|calendar|
  |54|camel|
  |55|camera|
  |56|camouflage|
  |57|campfire|
  |58|candle|
  |59|cannon|
  |60|canoe|
  |61|car|
  |62|carrot|
  |63|castle|
  |64|cat|
  |65|ceiling fan|
  |66|cell phone|
  |67|cello|
  |68|chair|
  |69|chandelier|
  |70|church|
  |71|circle|
  |72|clarinet|
  |73|clock|
  |74|cloud|
  |75|coffee cup|
  |76|compass|
  |77|computer|
  |78|cookie|
  |79|cooler|
  |80|couch|
  |81|cow|
  |82|crab|
  |83|crayon|
  |84|crocodile|
  |85|crown|
  |86|cruise ship|
  |87|cup|
  |88|diamond|
  |89|dishwasher|
  |90|diving board|
  |91|dog|
  |92|dolphin|
  |93|donut|
  |94|door|
  |95|dragon|
  |96|dresser|
  |97|drill|
  |98|drums|
  |99|duck|
  |100|dumbbell|
  |101|ear|
  |102|elbow|
  |103|elephant|
  |104|envelope|
  |105|eraser|
  |106|eye|
  |107|eyeglasses|
  |108|face|
  |109|fan|
  |110|feather|
  |111|fence|
  |112|finger|
  |113|fire hydrant|
  |114|fireplace|
  |115|firetruck|
  |116|fish|
  |117|flamingo|
  |118|flashlight|
  |119|flip flops|
  |120|floor lamp|
  |121|flower|
  |122|flying saucer|
  |123|foot|
  |124|fork|
  |125|frog|
  |126|frying pan|
  |127|garden hose|
  |128|garden|
  |129|giraffe|
  |130|goatee|
  |131|golf club|
  |132|grapes|
  |133|grass|
  |134|guitar|
  |135|hamburger|
  |136|hammer|
  |137|hand|
  |138|harp|
  |139|hat|
  |140|headphones|
  |141|hedgehog|
  |142|helicopter|
  |143|helmet|
  |144|hexagon|
  |145|hockey puck|
  |146|hockey stick|
  |147|horse|
  |148|hospital|
  |149|hot air balloon|
  |150|hot dog|
  |151|hot tub|
  |152|hourglass|
  |153|house plant|
  |154|house|
  |155|hurricane|
  |156|ice cream|
  |157|jacket|
  |158|jail|
  |159|kangaroo|
  |160|key|
  |161|keyboard|
  |162|knee|
  |163|knife|
  |164|ladder|
  |165|lantern|
  |166|laptop|
  |167|leaf|
  |168|leg|
  |169|light bulb|
  |170|lighter|
  |171|lighthouse|
  |172|lightning|
  |173|line|
  |174|lion|
  |175|lipstick|
  |176|lobster|
  |177|lollipop|
  |178|mailbox|
  |179|map|
  |180|marker|
  |181|matches|
  |182|megaphone|
  |183|mermaid|
  |184|microphone|
  |185|microwave|
  |186|monkey|
  |187|moon|
  |188|mosquito|
  |189|motorbike|
  |190|mountain|
  |191|mouse|
  |192|moustache|
  |193|mouth|
  |194|mug|
  |195|mushroom|
  |196|nail|
  |197|necklace|
  |198|nose|
  |199|ocean|
  |200|octagon|
  |201|octopus|
  |202|onion|
  |203|oven|
  |204|owl|
  |205|paint can|
  |206|paintbrush|
  |207|palm tree|
  |208|panda|
  |209|pants|
  |210|paper clip|
  |211|parachute|
  |212|parrot|
  |213|passport|
  |214|peanut|
  |215|pear|
  |216|peas|
  |217|pencil|
  |218|penguin|
  |219|piano|
  |220|pickup truck|
  |221|picture frame|
  |222|pig|
  |223|pillow|
  |224|pineapple|
  |225|pizza|
  |226|pliers|
  |227|police car|
  |228|pond|
  |229|pool|
  |230|popsicle|
  |231|postcard|
  |232|potato|
  |233|power outlet|
  |234|purse|
  |235|rabbit|
  |236|raccoon|
  |237|radio|
  |238|rain|
  |239|rainbow|
  |240|rake|
  |241|remote control|
  |242|rhinoceros|
  |243|rifle|
  |244|river|
  |245|roller coaster|
  |246|rollerskates|
  |247|sailboat|
  |248|sandwich|
  |249|saw|
  |250|saxophone|
  |251|school bus|
  |252|scissors|
  |253|scorpion|
  |254|screwdriver|
  |255|sea turtle|
  |256|see saw|
  |257|shark|
  |258|sheep|
  |259|shoe|
  |260|shorts|
  |261|shovel|
  |262|sink|
  |263|skateboard|
  |264|skull|
  |265|skyscraper|
  |266|sleeping bag|
  |267|smiley face|
  |268|snail|
  |269|snake|
  |270|snorkel|
  |271|snowflake|
  |272|snowman|
  |273|soccer ball|
  |274|sock|
  |275|speedboat|
  |276|spider|
  |277|spoon|
  |278|spreadsheet|
  |279|square|
  |280|squiggle|
  |281|squirrel|
  |282|stairs|
  |283|star|
  |284|steak|
  |285|stereo|
  |286|stethoscope|
  |287|stitches|
  |288|stop sign|
  |289|stove|
  |290|strawberry|
  |291|streetlight|
  |292|string bean|
  |293|submarine|
  |294|suitcase|
  |295|sun|
  |296|swan|
  |297|sweater|
  |298|swing set|
  |299|sword|
  |300|syringe|
  |301|t-shirt|
  |302|table|
  |303|teapot|
  |304|teddy-bear|
  |305|telephone|
  |306|television|
  |307|tennis racquet|
  |308|tent|
  |309|The Eiffel Tower|
  |310|The Great Wall of China|
  |311|The Mona Lisa|
  |312|tiger|
  |313|toaster|
  |314|toe|
  |315|toilet|
  |316|tooth|
  |317|toothbrush|
  |318|toothpaste|
  |319|tornado|
  |320|tractor|
  |321|traffic light|
  |322|train|
  |323|tree|
  |324|triangle|
  |325|trombone|
  |326|truck|
  |327|trumpet|
  |328|umbrella|
  |329|underwear|
  |330|van|
  |331|vase|
  |332|violin|
  |333|washing machine|
  |334|watermelon|
  |335|waterslide|
  |336|whale|
  |337|wheel|
  |338|windmill|
  |339|wine bottle|
  |340|wine glass|
  |341|wristwatch|
  |342|yoga|
  |343|zebra|
  |344|zigzag|

</details>

#### `sketch_rnn` and `sketch_rnn_full`

- `word`: Category the player was prompted to draw.
- `drawing`: An array of strokes. Strokes are represented as 3-tuples consisting of x-offset, y-offset, and a binary variable which is 1 if the pen is lifted between this position and the next, and 0 otherwise.

<details>
  <summary>
  Click here to see the code for visualizing drawings in Jupyter Notebook or Google Colab:
  </summary>

  ```python
  import numpy as np
  import svgwrite  # pip install svgwrite
  from IPython.display import SVG, display

  def draw_strokes(drawing, factor=0.045):
    """Displays vector drawing as SVG.

    Args:
      drawing: a list of strokes represented as 3-tuples
      factor: scaling factor. The smaller the scaling factor, the bigger the SVG picture and vice versa.

    """
    def get_bounds(data, factor):
      """Return bounds of data."""
      min_x = 0
      max_x = 0
      min_y = 0
      max_y = 0

      abs_x = 0
      abs_y = 0
      for i in range(len(data)):
        x = float(data[i, 0]) / factor
        y = float(data[i, 1]) / factor
        abs_x += x
        abs_y += y
        min_x = min(min_x, abs_x)
        min_y = min(min_y, abs_y)
        max_x = max(max_x, abs_x)
        max_y = max(max_y, abs_y)

      return (min_x, max_x, min_y, max_y)

    data = np.array(drawing)
    min_x, max_x, min_y, max_y = get_bounds(data, factor)
    dims = (50 + max_x - min_x, 50 + max_y - min_y)
    dwg = svgwrite.Drawing(size=dims)
    dwg.add(dwg.rect(insert=(0, 0), size=dims,fill='white'))
    lift_pen = 1
    abs_x = 25 - min_x
    abs_y = 25 - min_y
    p = "M%s,%s " % (abs_x, abs_y)
    command = "m"
    for i in range(len(data)):
      if (lift_pen == 1):
        command = "m"
      elif (command != "l"):
        command = "l"
      else:
        command = ""
      x = float(data[i,0])/factor
      y = float(data[i,1])/factor
      lift_pen = data[i, 2]
      p += command+str(x)+","+str(y)+" "
    the_color = "black"
    stroke_width = 1
    dwg.add(dwg.path(p).stroke(the_color,stroke_width).fill("none"))
    display(SVG(dwg.tostring()))
  ```

</details>


> **Note**: Sketch-RNN takes for input strokes represented as 5-tuples with drawings padded to a common maximum length and prefixed by the special start token `[0, 0, 1, 0, 0]`. The 5-tuple representation consists of x-offset, y-offset, and p_1, p_2, p_3, a binary one-hot vector of 3 possible pen states: pen down, pen up, end of sketch. More precisely, the first two elements are the offset distance in the x and y directions of the pen from the previous point. The last 3 elements represents a binary one-hot vector of 3 possible states. The first pen state, p1, indicates that the pen is currently touching the paper, and that a line will be drawn connecting the next point with the current point. The second pen state, p2, indicates that the pen will be lifted from the paper after the current point, and that no line will be drawn next. The final pen state, p3, indicates that the drawing has ended, and subsequent points, including the current point, will not be rendered.
><details>
>  <summary>
>  Click here to see the code for converting drawings to Sketch-RNN input format:
>  </summary>
>
>  ```python
>  def to_sketch_rnn_format(drawing, max_len):
>    """Converts a drawing to Sketch-RNN input format.
>
>    Args:
>      drawing: a list of strokes represented as 3-tuples
>      max_len: maximum common length of all drawings
>
>    Returns:
>      NumPy array
>    """
>    drawing = np.array(drawing)
>    result = np.zeros((max_len, 5), dtype=float)
>    l = len(drawing)
>    assert l <= max_len
>    result[0:l, 0:2] = drawing[:, 0:2]
>    result[0:l, 3] = drawing[:, 2]
>    result[0:l, 2] = 1 - result[0:l, 3]
>    result[l:, 4] = 1
>    # Prepend special start token
>    result = np.vstack([[0, 0, 1, 0, 0], result])
>    return result
>  ```
>
></details>

### Data Splits

In the configurations `raw`, `preprocessed_simplified_drawings` and `preprocessed_bitamps` (default configuration), all the data is contained in the training set, which has 50426266 examples.

`sketch_rnn` and `sketch_rnn_full` have the data split into training, validation and test split. In the `sketch_rnn` configuration, 75K samples (70K Training, 2.5K Validation, 2.5K Test) have been randomly selected from each category. Therefore, the training set contains 24150000 examples, the validation set 862500 examples and the test set 862500 examples. The `sketch_rnn_full` configuration has the full (training) data for each category, which leads to the training set having 43988874 examples, the validation set 862500 and the test set 862500 examples.

## Dataset Creation

### Curation Rationale

From the GitHub repository:

> The Quick Draw Dataset is a collection of 50 million drawings across [345 categories](categories.txt), contributed by players of the game [Quick, Draw!](https://quickdraw.withgoogle.com). The drawings were captured as timestamped vectors, tagged with metadata including what the player was asked to draw and in which country the player was located. You can browse the recognized drawings on [quickdraw.withgoogle.com/data](https://quickdraw.withgoogle.com/data).
>
> We're sharing them here for developers, researchers, and artists to explore, study, and learn from

### Source Data

#### Initial Data Collection and Normalization

This dataset contains vector drawings obtained from [Quick, Draw!](https://quickdraw.withgoogle.com/), an online game where the players are asked to draw objects belonging to a particular object class in less than 20 seconds.

#### Who are the source language producers?

The participants in the [Quick, Draw!](https://quickdraw.withgoogle.com/) game.

### Annotations

#### Annotation process

The annotations are machine-generated and match the category the player was prompted to draw.

#### Who are the annotators?

The annotations are machine-generated.

### Personal and Sensitive Information

Some sketches are known to be problematic (see https://github.com/googlecreativelab/quickdraw-dataset/issues/74 and https://github.com/googlecreativelab/quickdraw-dataset/issues/18).

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

## Additional Information

### Dataset Curators

Jonas Jongejan, Henry Rowley, Takashi Kawashima, Jongmin Kim and Nick Fox-Gieg.

### Licensing Information

The data is made available by Google, Inc. under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) license.

### Citation Information

```bibtex
@article{DBLP:journals/corr/HaE17,
  author    = {David Ha and
               Douglas Eck},
  title     = {A Neural Representation of Sketch Drawings},
  journal   = {CoRR},
  volume    = {abs/1704.03477},
  year      = {2017},
  url       = {http://arxiv.org/abs/1704.03477},
  archivePrefix = {arXiv},
  eprint    = {1704.03477},
  timestamp = {Mon, 13 Aug 2018 16:48:30 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/HaE17},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

### Contributions

Thanks to [@mariosasko](https://github.com/mariosasko) for adding this dataset.