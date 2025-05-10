import random

meditations_by_mood = {
    "sad": [
        "Try a Loving-Kindness Meditation.<br>1. Sit quietly and close your eyes.<br>2. Bring someone you love to mind.<br>3. Silently repeat phrases like: 'May you be happy. May you be safe. May you be peaceful.'<br>4. After a few minutes, direct those wishes to yourself.<br>5. Continue for 5-10 minutes.",

        "Listen to a guided meditation focused on self-compassion.<br>1. Find a quiet space and sit or lie down.<br>2. Put on headphones and select a self-compassion audio meditation.<br>3. Let the guide lead you through affirmations and deep breathing.<br>4. Reflect on the kind words being said to you.<br>5. Stay present and open to emotional release.",

        "Do a gratitude journaling meditation for 5 minutes.<br>1. Sit down with a notebook or digital journal.<br>2. Close your eyes and take a few deep breaths.<br>3. Think of three things you're grateful for today.<br>4. Write each one down and why it matters to you.<br>5. End with a moment of stillness and appreciation.",

        "Practice a body scan meditation.<br>1. Lie down or sit comfortably.<br>2. Close your eyes and take 3 deep breaths.<br>3. Bring attention to your feet and slowly move upward (legs, torso, arms, head).<br>4. At each area, notice sensations without judgment.<br>5. Breathe and release tension as you scan.",

        "Try a mindful crying session.<br>1. Allow yourself to feel your sadness fully.<br>2. Sit in a quiet space with tissues nearby.<br>3. Let the tears come without suppression.<br>4. As you cry, focus on the sensations — the tears, breath, heartbeat.<br>5. Afterward, place your hand on your heart and breathe deeply.",

        "Go on a mindful walk.<br>1. Choose a quiet path or park.<br>2. Walk slowly, observing the sensation of your feet on the ground.<br>3. Notice sounds, smells, and sights without judgment.<br>4. Breathe deeply and stay in the present moment.<br>5. Walk for 10–20 minutes.",

        "Use affirmation meditation.<br>1. Sit comfortably and close your eyes.<br>2. Choose an affirmation like 'I am worthy of love and healing.'<br>3. Inhale deeply and silently say it.<br>4. Exhale and repeat the affirmation.<br>5. Continue for 5–10 minutes.",

        "Do a breathing meditation with visual focus.<br>1. Light a candle or focus on a plant or object.<br>2. Sit comfortably and take deep breaths.<br>3. Inhale for 4, hold for 4, exhale for 6.<br>4. Keep your gaze soft and return to the object if distracted.<br>5. Repeat for 5–10 minutes.",

        "Hug yourself meditation.<br>1. Wrap your arms around yourself gently.<br>2. Close your eyes and breathe deeply.<br>3. Silently say kind things like 'I’m doing my best.'<br>4. Feel the warmth of your touch.<br>5. Hold for 1–2 minutes and slowly release.",

        "Heart rhythm meditation.<br>1. Place a hand on your heart.<br>2. Breathe in and imagine energy flowing into your chest.<br>3. Exhale slowly and release tension.<br>4. Match your breath with your heartbeat.<br>5. Continue for 5 minutes, focusing on love and calm."
    ]
    ,

    "anxious": [
        "Box Breathing:<br>1. Inhale through your nose for 4 seconds.<br>2. Hold your breath for 4 seconds.<br>3. Exhale through your mouth for 4 seconds.<br>4. Hold again for 4 seconds.<br>5. Repeat this cycle for 2-5 minutes.",

        "5-4-3-2-1 Grounding:<br>1. Look around and name 5 things you can see.<br>2. Touch 4 things and observe their textures.<br>3. Listen for 3 different sounds.<br>4. Identify 2 things you can smell.<br>5. Notice 1 thing you can taste.",

        "Progressive Muscle Relaxation:<br>1. Sit or lie down comfortably.<br>2. Start with your toes: tense for 5 seconds, then release.<br>3. Move upward—feet, calves, thighs, abdomen, chest, arms, hands, shoulders, neck, face.<br>4. Focus on releasing tension.",

        "Visualization Meditation:<br>1. Close your eyes and breathe slowly.<br>2. Picture a peaceful place (like a beach or forest).\br>3. Imagine yourself there: feel the air, hear sounds, notice colors.<br>4. Stay in this scene for 5-10 minutes.",

        "Mindful Walking:<br>1. Walk slowly and naturally.<br>2. Focus on your footsteps and your breath.<br>3. Notice the environment: colors, smells, sounds.<br>4. Walk for at least 5 minutes with awareness.",

        "Breath Awareness:<br>1. Sit or lie comfortably.<br>2. Focus on your breath entering and leaving your nostrils.<br>3. If thoughts distract you, gently bring your focus back to the breath.<br>4. Continue for 5-10 minutes.",

        "Affirmation Meditation:<br>1. Sit quietly.<br>2. Breathe deeply and say to yourself: 'I am safe', 'I am calm', 'I can handle this'.<br>3. Repeat affirmations with each breath for 5-10 minutes.",

        "Journaling Your Worries:<br>1. Write down what’s making you anxious.<br>2. Don’t filter—let thoughts flow.<br>3. Read what you wrote and ask: is this thought logical?<br>4. Counter with a rational, calming response.",

        "Listen to Nature Sounds:<br>1. Put on headphones and play sounds like ocean waves or rain.<br>2. Close your eyes and focus only on the sounds.<br>3. Let your mind wander peacefully for 5-10 minutes.",

        "Legs-Up-The-Wall Pose:<br>1. Lie on your back and place legs up against a wall.<br>2. Rest your arms at your sides.<br>3. Breathe deeply and relax for 10 minutes."
    ],

    "angry": [
        "Body Scan:<br>1. Sit or lie in a quiet space.<br>2. Close your eyes and bring attention to your toes.<br>3. Slowly move focus upward through your body, noticing tension.<br>4. Release tension as you go.",

        "Count-to-10 Breathing:<br>1. Inhale for 3 seconds.<br>2. Hold for 2 seconds.<br>3. Exhale slowly for 5 seconds.<br>4. Repeat while counting up to 10.<br>5. Focus on calming down with each count.",

        "Unsent Letter:<br>1. Write a letter to the person or situation that made you angry.<br>2. Don’t hold back, express everything.<br>3. Once done, read it if you like, then tear it up or delete it.",

        "Clenched Fist Release:<br>1. Clench your fists tightly for 10 seconds.<br>2. Notice the tension.<br>3. Slowly open your hands and let the anger release.<br>4. Repeat as needed.",

        "Walking Meditation:<br>1. Take a brisk walk.<br>2. With every step, say silently: 'I choose peace' or 'Let it go'.<br>3. Feel your body releasing anger.<br>4. Walk for at least 10 minutes.",

        "Cooling Breath:<br>1. Curl your tongue like a straw.<br>2. Inhale deeply through the tongue.<br>3. Exhale through your nose.<br>4. Do this for 5-10 rounds to cool down emotionally.",

        "Sound Release:<br>1. Go to a private place.<br>2. Scream into a pillow or hum loudly on the exhale.<br>3. Repeat until you feel a sense of emotional release.",

        "Draw Your Anger:<br>1. Grab paper and bold-colored pens.<br>2. Let your hands express your feelings with wild lines or shapes.<br>3. Don’t judge what comes out — just feel the process.",

        "Gratitude Flip:<br>1. Pause and write 3 things you are grateful for.<br>2. Say them aloud.<br>3. Feel the shift in energy from anger to appreciation.",

        "Shower Reset:<br>1. Take a warm shower.<br>2. As water runs down, imagine your anger washing away.<br>3. Visualize calm energy replacing it."
    ],
    "stressed": [
        "Mini-Meditation:<br>1. Close your eyes.<br>2. Inhale slowly for 4 seconds, hold for 2, exhale for 6.<br>3. Do this for 10 slow breaths.<br>4. Focus only on breathing.",

        "Shoulder Roll Breathing:<br>1. Inhale and roll shoulders up.<br>2. Exhale and roll them down and back.<br>3. Repeat 10 times while keeping breath smooth.",

        "Calm Jar Exercise:<br>1. Shake a glitter jar or snow globe.<br>2. Watch the particles slowly settle.<br>3. Breathe deeply as you observe.<br>4. Imagine your thoughts settling too.",

        "Body Relaxation Audio:<br>1. Play a guided body relaxation track.<br>2. Lie down and follow the voice.<br>3. Let tension release from each area of your body.",

        "Tea Ritual:<br>1. Prepare a herbal tea like chamomile or mint.<br>2. Notice the smell, color, and warmth.<br>3. Drink slowly, focusing on the experience.",

        "Stretch & Breathe:<br>1. Do a few gentle stretches (neck rolls, side bends, forward fold).\br>2. Inhale as you stretch up, exhale as you release.<br>3. Continue for 5-10 minutes.",

        "Music Therapy:<br>1. Find slow instrumental or nature music.<br>2. Lie in a quiet room and close your eyes.<br>3. Let the sound soothe your nervous system for 10 minutes.",

        "Mantra Meditation:<br>1. Sit comfortably.<br>2. Repeat a word like 'peace', 'relax', or 'let go' with each breath.<br>3. Continue for 5-10 minutes.",

        "Tapping (EFT):\br>1. Tap gently on points: side of hand, under eye, top of head.<br>2. While tapping, say your stress aloud (e.g., 'I'm overwhelmed').<br>3. Repeat until you feel calmer.",

        "Do Nothing:<br>1. Sit or lie down with no goal or task.<br>2. Turn off your phone.<br>3. Let your mind drift.<br>4. Give yourself permission to just exist for 5-10 minutes."
    ],

    "happy": [
        "Amplify the Joy:<br>1. Sit comfortably and close your eyes.<br>2. Recall what’s making you happy.<br>3. Breathe deeply and soak in the feeling.<br>4. Say: 'I am grateful for this joy.'<br>5. Stay in the feeling for 2-5 minutes.",

        "Share the Positivity:<br>1. Think of someone who could use some kindness.<br>2. Send a short message, compliment, or positive note.<br>3. Let your happiness ripple outward.",

        "Joyful Movement:<br>1. Put on your favorite upbeat song.<br>2. Dance freely—no rules.<br>3. Feel the rhythm and let your body express the joy.",

        "Laughter Meditation:<br>1. Sit with a light smile.<br>2. Start by fake-laughing.<br>3. Let it grow into real laughter.<br>4. Continue laughing for 2-3 minutes.<br>5. End with deep breaths and a smile.",

        "Gratitude Expansion:<br>1. List 5 things you’re grateful for right now.<br>2. Reflect on how they bring happiness.<br>3. Close your eyes and feel the thankfulness.",

        "Heart-Centered Breathing:<br>1. Place your hand on your heart.<br>2. Inhale slowly through the nose.<br>3. Exhale gently through the mouth.<br>4. Imagine your heart glowing with warmth and joy.<br>5. Continue for 5 minutes.",

        "Happy Memory Replay:<br>1. Sit quietly.<br>2. Visualize a moment when you felt extremely happy.<br>3. Replay the sights, sounds, and emotions.<br>4. Let the memory lift your mood further.",

        "Nature Connection:<br>1. Go outside or sit near a window.<br>2. Observe the beauty of nature.<br>3. Breathe deeply and feel connected to the present moment.",

        "Creative Burst:<br>1. Pick a creative task: doodle, write a poem, hum a tune.<br>2. Let your emotions flow into the activity.<br>3. Embrace the process, not the result.",

        "Smile Awareness:<br>1. Smile gently.<br>2. Notice how your body reacts.<br>3. Keep the smile for 2 minutes and breathe slowly.<br>4. Let it infuse you with even more joy."
    ],

    "neutral": [
        "Mindful Check-In:<br>1. Sit still and close your eyes.<br>2. Ask yourself: How do I feel right now?<br>3. Observe without judgment.<br>4. Breathe slowly and note any subtle emotions.",

        "Body Awareness Scan:<br>1. Start from your toes.<br>2. Slowly bring attention to each body part upward.<br>3. Notice sensations, tensions, or comfort.<br>4. Continue for 5-10 minutes.",

        "Balanced Breath:<br>1. Inhale for 4 seconds.<br>2. Exhale for 4 seconds.<br>3. Keep the rhythm even and smooth.<br>4. Repeat for 5 minutes to build calm clarity.",

        "Color Observation:<br>1. Pick a color (e.g., blue).\br>2. Look around and spot everything with that color.<br>3. Stay present and aware as you observe.<br>4. Let it be a mini visual meditation.",

        "Sound Focus:<br>1. Sit in silence.<br>2. Tune into all sounds around you.<br>3. Don’t label or analyze—just listen.<br>4. Focus for 2-3 minutes.",

        "Palm Awareness:<br>1. Rub your palms together to create warmth.<br>2. Hold them slightly apart and feel the energy.<br>3. Slowly bring them close and apart, observing the sensation.",

        "One-Minute Mindfulness:<br>1. Stop everything.<br>2. Breathe deeply and be fully present.<br>3. Observe your breath, your posture, your environment.<br>4. Reset with just a minute of stillness.",

        "Mindful Eating:<br>1. Take one bite of something (like a fruit).\br>2. Chew slowly and observe texture and flavor.<br>3. Stay focused only on eating.<br>4. Appreciate the moment.",

        "Step Counting Walk:<br>1. Walk slowly and count your steps silently.<br>2. Match each step with your breath.<br>3. Stay aware of the contact of feet with the ground.",

        "Silent Sitting:<br>1. Sit with a straight spine.<br>2. Rest hands on your lap.<br>3. Do nothing—no phone, no thinking, just being.<br>4. Stay in stillness for 5-10 minutes."
    ]

}

def get_random_meditation(mood):
    mood = mood.lower()
    options = meditations_by_mood.get(mood, meditations_by_mood['neutral'])
    return random.choice(options)