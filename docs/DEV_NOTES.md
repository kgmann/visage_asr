# Speech Recognition System

## Overview

The purpose of the project is to create a Speech Recognition System for the local language FONGBE. It's a part of a biggest project which consist to create a Speech to Speech Translation System with three modules ***(ASR + MT + TTS)***.
We took a modular approach for the speech to speech translation system and it leads us to decide to use web services so that each component is as indepedent as possible from the other ones.
This web service is the ASR part and is independent from the other ones. It can then be used standalone with other apps.

## Model's description

We've used kaldi to create the Speech Recognition model. If you have never eared about it or used it before don't worry, I didn't before starting working on it too ;). You won't propably need high knowledge in NLP (especially ASR) before getting started with Kaldi.
Here are some useful resources to get started with kaldi [kaldi website](https://kaldi-asr.org/).
This is obviously a short list and you need to check additional resources if you have to work on Specch recognition models with kaldi.

Now let's give a short description of what I did with kaldi.
When I started working on the project I first searched for differents tools to build a Speech Recognition model. I found several ones and I chose CMUSphinx. That choice was mainly guided by the fact that CMUSphinx has been for several years a state of the art speech recognition tool (even if it's not the case anymore, I think.). In addition to that, it has a pretty large community and finally it's easier to get started with CMUSphinx in comparision to the other tools available ;). But approximately two months after I started, I found out that it will be almost impossible to work with CMUShpinx and build a working speech recogntion system for FONGBE. That's because there were almost zero resources on speech recognition in FONGBE with CMUSphinx and in addition to that, after crafting for a time I found out that I may need to have pretty good background in speech recognition to be able to set everything up ***"from scratch"***. I finally decided to find a more viable solution and after searching a bit I discovered the [ALFFA Project](http://alffa.imag.fr) and a [FONGBE dataset](https://github.com/besacier/ALFFA_PUBLIC/tree/master/ASR/FONGBE).

The [FONGBE dataset](https://github.com/besacier/ALFFA_PUBLIC/tree/master/ASR/FONGBE) is a set of ressources to create a speech recognition system in FONGBE. The tool used to create the model is kaldi. To make it short I read a bunch of stuff on kaldi after installing it. (*Quick tip*: Intalling kaldi with docker will probably make you save years of turmoils, thank me later ;)). I made some test with it and I finally trained the **monophone** model decribed [here](https://github.com/besacier/ALFFA_PUBLIC/tree/master/ASR/FONGBE). It' actually the less acurate of the list but we were under time constraint so I decided to create the web App with it first.

The second part, after creating the model, was to use it to create a web app. kaldi is mainly created with C++ and bash. There are some wrappers in python and after making some comparisions I decided to go for [pykaldi](https://github.com/pykaldi/pykaldi) and I went through its [documentation](https://pykaldi.github.io/). After spending some time on it I finally make it work and I created the Flask application.

## App's description

We created an API with flask and we made a quick webapp to make a live test by uploading an audio file in a form. Having separation in concern, we decided to create the application and make it as model agnostic as possible.
The application needs three model files to be able to recognize speech. The path of those files are in the application's configurations in the file "***config.py***". So all we need to do in order to improve the recognition's accuracy is to update the model (or create a new one) and replace the required file in the application.
After it's done we can deploy again and the new model will be used.

**NB :** There is still a little concern about how to handle the model's file in the repository. There are many solutions to handle binary files in a git repository but that is not really a concern right now. However we should take it in consideration in the next commits as the application starts growing.
For further details, check the [API's documentation](https://github.com/MIFY-AI/visage-asr/blob/develop/docs/API_DOCS.md) on the git repository or on the website.

## Further additionnal stuff

Here is a short list of additional stuff to add to the web app for further enhancements.

- Try to write as clean code as possible to keep the app easily scalable and maintaible ;).

1. Use celery to make translations in the web app. (Translations are actually being done in the main thread of the web application and this is actually not a good way to handle possibly heavy computations).

2. Think about adding new options to the "config" parameter of the API and extend it with new features (I inspired myself from the Google Speech Recognition API. You can take a look at it ;)).

3. Think about adding tests (Just a suggestion, not a debate about their usefulness :)).
