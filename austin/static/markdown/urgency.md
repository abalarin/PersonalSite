# How Does this Model Work?
### Layers:
- One-Hot-Encoding
- Padding
- Embedding
- 1D Convolution
- Flatten
- Densely Connected layer 1 of size 250
- Densely Connected layer 2 of size 1

## One-Hot-Encoding
> *While this may not technically be considered a Keras layer, a transformation of the original input occurs, and I'm considering it layer from a practicality standpoint.*

Once a text body is parsed into and array of size **n** words ie: ["A", "Quick", "Brown" ... n], a filter of sorts is applied that maps every word to its respective index in a vocabulary.

An example conversion for a text with a vocabulary size 10,000 might look like the following:

1. "A quick brown fox jumps over the fence"
2. ["A", "quick", "brown", "fox", "jumps", "over", "the", "fence"]
3. [1, 5303, 9410, 9492, 7585, 5776, 520, 3212]

Where every word is mapped to an index between 1 and 10,000

## Padding
> *Same as one-hot-encoding, this is technically not a Keras layer, but a transformation is performed...*

Since every input might be a different length of words, when we pass it though the convolutional layers of our network (and reduce vector size) we would like to preserve some characteristics of the original pattern of text. We also want to kinda normalize the first convolution by standardizing the input.

So if we say the padding is the size of the maximum amount of words in a single input, lets say 100, we might get an output like the following:

1.  ["A", "quick", "brown", "fox", "jumps", "over", "the", "fence"]
2.  [1, 5303, 9410, 9492, 7585, 5776, 520, 3212]
3.  [   0    0    0    0    0    0    0    0    0    0    0    0    0    0
        0    0    0    0    0    0    0    0    0    0    0    0    0    0
        0    0    0    0    0    0    0    0    0    0    0    0    0    0
        0    0    0    0    0    0    0    0    0    0    0    0    0    0
        0    0    0    0    0    0    0    0    0    0    0    0    0    0
        0    0    0    0    0    0    0    0    0    0    0    0    0    0
        0    0    0    0    0    0    0    0    1 5303 9410 9492 7585 5776
     520 3212]
