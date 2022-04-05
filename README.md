# Evaluating Taekwondo Moves

This system aims to recognize and evaluate 10 foundational taekwondo moves through the following modules based on Bianco & Tisato's 2013 article "Karate Moves Recognition from Skeletal Motion": Skeleton Representation, Pose Classification, and Temporal Alignment.

*Developed in the TJHSST Computer Systems Research Lab 2020-21

## Skeleton Recognition

System extrapolate the 3D coordinates of joints in an athlete’s body from the 2D coordinates identified by Detectron for a given sample video through [Facebook’s VideoPose3D](https://github.com/facebookresearch/VideoPose3D) model.

## Pose Classification

System classifies categorizes a performed move (ex. A front kick has three parts: knee-up/chamber, extension, re-chamber) into one of the 10 techniques based on key poses identified through K-means and K-nearest neighbors.

## Temporal Alignment &  Scoring

System compares the performed sequence of poses to exemplar poses with Dynamic Time Warping and outputs a similarity score as the final evaluation.
