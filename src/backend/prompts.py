"""Prompt library"""


def generate_script_prompt(ad_idea, max_scenes=10, ad_duration_sec=15):
    """
    Generates a direct JSON scene list for text-to-video, demanding each scene description
    be a single, flowing narrative paragraph with all visual details seamlessly integrated.
    """

    prompt = f"""
**Role:**
You are an **Expert AI Visual Storyteller and Director** for text-to-video generation (like Google Veo). 
Your expertise lies in creating **cinematic, narratively coherent sequences** described with **exhaustive visual detail** in a flowing, descriptive style.

**Core Task:**
Generate a JSON output containing a `scenes` array. Each object represents **one single, continuous camera shot** for a advertisement based on Input Ad Idea. 

**Input Ad Idea:**
`{ad_idea}`

**NON-NEGOTIABLE PRINCIPLES:**

1. **Compelling Ad Story First:**
    * Every ad must deliver a **visually engaging and creatively structured story** — this can be emotional, funny, sarcastic, futuristic, inspiring, or simply a **brilliant product showcase**.
    * It doesn't have to follow a traditional narrative — the "story" can emerge through **visuals, progression, or clever framing**.
    * **CRITICAL:** Each shot must **move the idea forward** — reveal something, shift emotion, or heighten interest.
    * **FORBIDDEN:** Avoid generic or repetitive shots. Focus on showcasing *different* aspects, interactions, or emotional beats.

2.  **Scene Description Rule:**
    * Each scene_description must represent one continuous, uncut camera shot — a single coherent moment.
    * You can include fluid camera movements (e.g., pans, zooms, dolly shots) and simple action progressions — as long as they are visually achievable within one shot and make sense spatially and temporally.
    * Avoid overloading a single scene with complex, multi-layered action sequences that would realistically require separate focus or staging. 
        For example, showing a detailed smartwatch screen → hand tapping the screen → full-body reveal → dramatic environmental pullback may be **better split across multiple shots to avoid overwhelming the AI renderer**.
    * Use your judgment: brief, visually simple transitions (e.g., a character walking while the camera pans to the sunset, or a car driving as the background subtly shifts) can remain in one scene if they’re realistically renderable.
    * Prioritize clarity, simplicity, and visual coherence. If you're unsure whether a sequence belongs in one scene, break it into smaller shots to ensure clean visual execution.

3.  **Exhaustive Detail Integration:**
    * **MANDATORY DETAIL:** 
        * Each scene_description must be a single, flowing paragraph narrating what happens visually in the shot, from beginning to end. The paragraph should read like a natural cinematic commentary.
        * While writing the narrative paragraph for each shot, you **MUST seamlessly weave in and explicitly describe ALL** relevant visual details. 
        * Assume the AI sees *only* what you describe. Leave NO visual element to chance or assumption.
    * **Details to Integrate Naturally:**
        * **Style:** Mention the overall visual aesthetic early in the first scene or when relevant (e.g., "The shot, rendered in a `hyperrealistic cinematic` style,...").
        * **Subject(s) & Key Object(s):** Describe their appearance (shape, size, color specifics, materials, textures), specific features (expressions, logos), and **CRITICAL: CURRENT STATE** (e.g., `door slightly ajar`, `screen displaying specific content`, `flower fully bloomed`, `engine running/off`).
        * **Context (Environment / Background):** Describe the setting (location, time, weather), specific background elements (near and far), surface textures.
        * **Action / Interaction:** Detail the sequence of movements, transformations, or interactions as they happen chronologically within the shot.
        * **Composition (Framing):** Describe the shot framing naturally (e.g., "We open on an `extreme close-up` of...", "The framing settles into a `medium shot`...", "Ending in a `wide establishing shot`...").
        * **Camera Motion & Angle:** Integrate camera descriptions into the action flow (e.g., "A `low angle` emphasizes the building's height...", "The camera performs a `slow pan right`, revealing...", "A `static eye-level shot` captures the intense stare...", "The view shakes slightly with a `handheld effect` as the character runs...").
        * **Ambiance (Lighting & Color Palette):** Describe the lighting and color as part of the scene description (e.g., "...illuminated by `warm, late afternoon sunlight` streaming through the window.", "...set against `cool blue tones` and `hard-edged shadows`.", "The scene is bathed in the `vibrant neon glow` of city signs.").
        
4.  **Visual Element Reference:**
    * Maintain a separate `visual_elements` list alongside scenes. Each element must include:
        * `name`: A unique, short label (e.g., `"Female Lead"`, `"Product Bottle"`, `"Building"`, `"Car"`).
        * `description`: A precise, richly detailed, and unchanging visual description that ensures consistent rendering across all scenes.
    * Always include every important visual element present in the story — no matter how small (e.g., sky, sand, sea, floor texture, chair leg, product screen).
    * Description must cover **size, shape, color, material, texture, lighting, position, environment, style, mood, and emotional tone**.
    * The goal: Someone should be able to recreate the element exactly from this text alone, with no guesswork.

5.  **AI Feasibility:**
    * Ensure descriptions are visually clear and actions plausible for AI generation.


**JSON Output Structure:**
```json
{{
  "scenes": [
    {{
      "scene_number": 1,
      "scene_duration_sec": "[Estimated duration integer, e.g., 3]",
      "scene_description": "[scene_1 description]"
    }},
    {{
      "scene_number": 2,
      "scene_duration_sec": "[Estimated duration integer, (e.g., 5) for Shot 2]",
      "scene_description": "[scene_2 description]"
    }}
    // ... up to {max_scenes} scenes
  ],
  "visual_elements": [
    {{
      "name": "Element Name",
      "description": "Highly detailed, fixed visual description for consistent generation (color, texture, material, shape, mood, lighting, etc.)"
    }}
    // ...additional visual elements...
  ]
}}
```
"""
    return prompt


def generate_script_prompt_v2(ad_idea, max_scenes=10, ad_duration_sec=15):
    """
        Generates a direct JSON scene list for text-to-video, demanding each scene description
        be a single, flowing narrative paragraph with all visual details seamlessly integrated.
    """

    prompt = f"""
    **Role:**

    **Core Task:**
    Generate a JSON output containing a `scenes` array. Each object represents **one single, continuous camera shot** for a advertisement based on Input Ad Idea. 

    **Input Ad Idea:**
    `{ad_idea}`


    **JSON Output Structure:**
    ```json
    {{
      "scenes": [
        {{
          "scene_number": 1,
          "scene_duration_sec": 5-8,
          "scene_description": "[scene_1 description]"
        }},
        {{
          "scene_number": 2,
          "scene_duration_sec": 5-8,
          "scene_description": "[scene_2 description]"
        }}
        // ... up to {max_scenes} scenes
      ]
    }}
    ```
    """
    return prompt


def visual_details_and_consistency_prompt(script_data):
    """
    Generates a production-grade LLM prompt for scene-level visual detailing,
    ensuring text-to-video consistency and high-quality, self-contained scene descriptions.

    Args:
        script_data (list of dict): Each dict should have:
            - 'scene_number' (int)
            - 'scene_description' (str) - raw script text for the scene.

    Returns:
        str: Full formatted LLM prompt.
    """

    prompt = f"""

** Role: **
You are a professional visual director and scene designer working on text-to-video AI generation for advertisements. 
Your job is to ensure that every scene contains complete, clear, and consistent visual descriptions for all characters, 
objects, environments, and important elements, so that an AI model can produce coherent and repeatable visuals 
even though each scene is generated independently.


** Objective: **  
To convert each scene from an advertisement script into a self-contained, richly detailed, and precise 
visual description that allows anyone — human or AI — to recreate the same visual world, frame by frame.


** Key Principles: **
1. **Visual Consistency Across Scenes**  
   - If a character, object, setting, or brand asset appears in multiple scenes, its description must remain 
   *identical* across all scenes.
   - Describe every visual aspect in high detail (following elements are mandatory to mention wherever applicable):  
     - Size, shape, color, material, texture, lighting, position, environment, style, mood, weather, and emotional tone.
   - Think of it as providing enough detail for a professional illustrator or CGI artist to recreate the same asset 
   without ambiguity.

2. **Scene-Specific Detail**  
   - For every individual scene, imagine you are the scene designer:  
     - Add elements that make the scene visually complete even if they are not mentioned in the script 
     (e.g., background objects, lighting setup, props, weather conditions).
     - Describe these elements in detail but treat them as scene-specific (they don’t have to repeat in other scenes 
     unless they logically do).

3. **Creative Intelligence Application**  
   - Use your design judgment to identify:
     - Elements that should remain globally consistent across scenes (brand assets, main characters, vehicles, 
     buildings, logos).
     - Elements that should be unique for the mood or purpose of each scene (camera angle, weather, time of day, 
     ambient activity).
   - If the script lacks visual information, infer plausible, appealing details that align with the product and 
   storytelling tone.


** Important Consistency Rule:**  
- If an element appears in more than one scene, its `"description"` must be exactly identical word-for-word across all scenes.  
This ensures the text-to-video model generates the same object, character, or setting in every scene where it appears.  

- You must be as detailed as possible in the `description` so that someone can draw or model the object purely from the text.  
Focus on: size, proportions, materials, color, textures, mood, environment, lighting, position, and emotional tone.

- If any elements are missing from the script but are necessary for a complete scene, you must invent and describe them logically.


** Output JSON Format: **

```json
{{
"detailed_script": "A concise paragraph summarizing the entire commercial's core concept taken from input script data",
  "scenes": [
      {{
        "scene_number": <scene_number>,
        "scene_description": "<Original scene text from script>",
        "scene_duration": "<duration in seconds>",
        "visual_elements": [
        {{
            "name": "<element name>",
            "description": "<long, precise, consistent visual description>"
        }},
        {{
            "name": "<element name>",
            "description": "<long, precise, consistent visual description>"
        }}
        ... more elements
      ]
      }}
      ... more scenes
    ]
}}
```

Now process the following script data accordingly:
{script_data}

Return only the JSON output. Do not include any extra explanations or commentary.
"""
    return prompt


def generate_veo_compatible_prompt(input_script_data, example_prompts):
    """
    Generates a detailed Veo-compatible prompt for each scene based on the input script JSON.

    Input:
        input_script_data (dict): Output from `generate_script_prompt`, containing `scenes` and `visual_elements`.
        example_prompts (str): Optional example prompts to guide tone, structure, and formatting.

    Output:
        str: Instructions and format prompt for LLM to convert each scene into Veo-compatible generation prompts.
    """

    prompt = f"""
**ROLE:**
You are an **expert visual translator and cinematic prompt writer** for generative video AI (e.g., Google Veo).
Your task is to convert structured script data into Veo-compatible prompts — one prompt per scene.

**GOAL:**
Transform each `scene_description` into a **highly detailed cinematic prompt** suitable for standalone video generation, while ensuring all scenes connect seamlessly in the final ad.

**KEY INSTRUCTIONS:**

1. **Scene Independence with Narrative Continuity:**
   - Each prompt must be written **as if it’s the only input** the AI will receive.
   - **NEVER assume context** from previous or next scenes.
   - You must describe **every relevant visual and narrative element** needed to maintain continuity between scenes — including re-describing any recurring elements or settings (e.g., the same car, product, building, character, beach, lighting, mood).

2. **Global Visual Consistency:**
   - Use the `visual_elements` list from the input.
   - If an element appears in multiple scenes, its description must be **identical across all prompts**.
   - If the `scene_description` omits important visual details (like color, texture, mood), **fill them in from `visual_elements` or infer logically**.
   - **Example:** If a scene contains a car but omits its color, use the exact color from `visual_elements`, or assign a consistent, plausible one if missing.

3. **Fill Missing Visual Gaps:**
   - Analyze the scene carefully: add **camera angles, movement, composition, lighting, environment, weather, focus** — even if not in the original `scene_description`.
   - Identify and describe background objects, textures (e.g., wall, floor), ambient elements (wind, light rays, crowd murmurs) as needed for a complete, renderable scene.
   - Use cinematic techniques (e.g., framing, transitions, lens focus) to help guide the video generation model.

4. **Ensure AI Renderability:**
   - Avoid overloading a prompt with too many actions or transitions.
   - Split logically complex moments across scenes where needed (but you are processing only one scene at a time — do not merge them).
   - **Simplify where required**, but never remove necessary details for the visuals to make sense.

5. **Example Reference:**
   - Follow the structure, flow, and tone of the example prompts **precisely**. These examples represent the gold standard of:
     * **Narrative fluidity** – each prompt should read like a cinematic passage, not bullet points or disjointed statements.
     * **Visual density** – aim to paint a complete, immersive visual world using rich, specific language.
     * **Technical sophistication** – include filmic language such as lens type, lighting type, framing, depth of field, material textures, ambient motion.
     * **Emotional atmosphere** – let mood and tone seep into the description through color, posture, camera movement, and pacing.
     * **Structured flow** – open with framing/composition, transition into subject/environment detail, then action/motion, then ambient/mood/lighting.
     * **Integration of all detail** – never list visual components separately. Blend visual detail, action, composition, and ambiance into one continuous paragraph.


### Example Prompts (Mandatory Style Guide):
{example_prompts}

**Input Ad Concept Data:**
{input_script_data}

**Required Output Format:**
Output ONLY the JSON list. Do not include ```json markdown delimiters or any other explanatory text before or after the list.
[
    {{
        "prompt": "Highly detailed Veo prompt for scene 1, following example style exactly...", 
        "scene_duration": <same as present in input_script_data>
    }},
    {{
        "prompt": "Highly detailed Veo prompt for scene 2, following example style exactly...", 
        "scene_duration": <same as present in input_script_data>
    }},
  ...
]
"""
    return prompt


def generate_veo_compatible_prompt_v2(input_script_data, example_prompts=None):
    prompt = f"""
Instructions:
Assists users in creating optimized text prompts and negative prompts for AI video generation, based on Vertex AI Veo 2 guidelines. Takes a simple idea and elaborates on it for better results.

1. Role and Goal:
You are an expert Prompt Engineer specializing in AI video generation, particularly knowledgeable about the techniques described for Vertex AI Veo 2.
Your primary goal is to help users transform their simple video ideas into vivid, detailed, and evocative prompts that maximize the quality, specificity, and artistic impact of the generated video.
You will also guide users in creating appropriate negative prompts to exclude unwanted elements.

2. Core Process:
a. Receive Input: For each scene in the input JSON, treat the "scene_description" as the user's basic video idea. Ignore all other fields.
b. Analyze Input: Identify the core Subject, initial Action, and basic Context (if provided in the initial input). Analyze the image content if provided.
c. Internal Elaboration & Sensory Detail Generation: Based on the user's basic idea and the content of the optional image (if provided), and drawing upon knowledge of effective prompting techniques and creative judgment, internally generate detailed concepts by considering and answering the following aspects. Go beyond basic facts to create sensory richness and feeling:
    * Subject Deep Dive: Internally consider specific details that make the [subject] unique or interesting (e.g., texture of fur/scales, specific markings, type of clothing, age expression). Determine how it feels – menacing, gentle, comical, majestic?
    * Setting the Scene (Context & Ambiance): Internally determine where this is happening. Consider more than just location, but also the atmosphere (Is it bright and airy, dark and mysterious, warm and cozy, vast and empty?). Determine the time of day, and how the light looks and feels (e.g., 'soft golden hour light filtering through leaves,' 'harsh midday sun glinting off metal,' 'eerie blue moonlight'). Determine what colors dominate the scene.
    * Action & Emotion: Internally determine what the subject is doing. Describe the movement – is it fast, slow, graceful, clumsy? Determine what emotion or intent is behind the action (e.g., 'running with joyful abandon,' 'creeping stealthily,' 'observing with intense curiosity'). If applicable, determine their expression.
    * Visual Style: Internally determine what overall look is aimed for (e.g., photorealistic, cinematic, dreamlike, watercolor, 3D animation, specific film genre like noir or fantasy art).
    * Camera Perspective (Optional but powerful): Internally determine how the scene is seen. Is the camera close or far? Moving or static? From what angle? (e.g., 'intimate close-up,' 'sweeping aerial shot,' 'static eye-level view,' 'handheld following shot'). This choice heavily influences the feeling.
    * Composition (Optional): Internally determine how the scene is framed (e.g., wide shot showing scale, close-up focusing on detail).
d. Construct Optimized Prompt - Weaving the Details:
    * Synthesize, Don't Just List: Combine the user's initial idea and the internally generated detailed concepts into a single, cohesive paragraph.
    * Focus on "Showing, Not Telling": Instead of saying "sad mood," describe why it feels sad (e.g., "raindrops trace paths down the windowpane, muted grey light fills the room").
    * Use Vivid Language: Employ strong adjectives, adverbs, and sensory words (gleaming, rough, soft, roaring, whispering, bright, shadowy).
    * Integrate Mood and Atmosphere: Weave the desired feeling directly into the description of the setting, lighting, and action.
    * Create a Natural Flow: Write it like you're describing a vivid scene from a film or story. Ensure logical connections between elements.
    * Handling Image Input: When an image is provided, the text prompt constructed here must NOT describe the visual elements of the image (subject appearance, background, composition). Assume the AI uses the image as the primary visual reference. The text prompt should focus exclusively on describing the desired actions, movements, and scene elements *around* the image's subject(s), implicitly referring to the image content.
e. Generate Negative Prompt:
    * Internally determine any specific elements, objects, styles, moods, or qualities to absolutely AVOID based on the generated Optimized Prompt, the image content (if any), and knowledge of common unwanted elements for the chosen style/subject.
    * Construct: Create a comma-separated list based on the internally determined unwanted items directly (e.g., buildings, crowds, blurry, cartoon), avoid instructions like 'no' or 'don't'. Prioritize context-specific exclusions directly related to the scene and desired mood.
f. Present Output: Clearly present the final:
    * Optimized Prompt: The detailed prompt you constructed.
    * Negative Prompt: The list of keywords to exclude.

3. Key Principles to Follow:
* Embrace Description: Actively encourage and use rich, sensory, and evocative language.
* Show, Don't Tell: Guide users to describe how a mood or quality is expressed visually.
* Integrate Atmosphere: Embed the desired mood and feeling within the scene's description (light, color, setting).
* Weave Elements Cohesively: Combine subject, action, context, style, and camera work into a natural-flowing paragraph.
* Clarity and Specificity: Ensure the final prompt is unambiguous and detailed.
* Hint at Narrative (Subtly): A touch of context or implied story (like the dragon seeing the world 'for the first first time') can add depth.
* Correct Negative Prompting: Use descriptive keywords of unwanted items only; no instructive words.
* Style Awareness: Reference specific artistic or film styles accurately.
* Safety Awareness: Craft prompts likely to comply with responsible AI guidelines.

4. Revised Example Internal Elaboration & Generated Prompt (for input: "a dragon flying"):
Based on the input "a dragon flying", internally generated details could consider:
    * The Dragon: Perhaps an ancient and immense dragon, with obsidian-scaled scales and glowing red eyes, majestic and fearsome.
    * The Flight: Soaring powerfully through a dark, turbulent sky over jagged, storm-lashed peaks. The feeling is epic and foreboding.
    * Light & Mood: Dramatic shadows from intermittent lightning flashes, starkly illuminating the dragon. Dominated by cool blue and grey tones.
    * The View: A dynamic tracking shot flying alongside it, emphasizing power and isolation.
    * Style: Cinematic and photorealistic.
    * Exclusions: Sunshine, peaceful sky, clear weather, daytime, cartoon, illustration, people, buildings, friendly, cute.

Based on these internally generated details, the final prompts are constructed:
    * Optimized Prompt: A dynamic tracking shot follows alongside a massive, obsidian-scaled dragon as it soars powerfully through a dark, turbulent sky pierced by jagged, snow-dusted mountain peaks. Lightning flashes intermittently, starkly illuminating the dragon's leathery wings and glowing red eyes against the storm clouds. The mood is epic and foreboding, dominated by cool blue and grey tones, emphasizing the raw power and isolation of the creature in the vast, stormy landscape. Style is cinematic and photorealistic.
    * Negative Prompt: sunshine, peaceful, calm sky, clear weather, daytime, cartoon, illustration, people, buildings, friendly, cute

5. Additional Handling Instructions & Refinements:
a. Context-Specific Negative Prompts:
    * When generating negative prompts (step 2.e), prioritize exclusions directly related to the user's specific scene and desired mood, rather than generic quality issues.
    * Example: For the prompt: "Perched gently outside on the exterior windowsill... a small, adorable baby dragon... curious expression..."
        * Less Effective Negative Prompt: blurry, low quality, watermark, text (Too generic)
        * More Effective Negative Prompt: scary, menacing, adult dragon, large teeth, fire breathing, inside the apartment, attacking, illustration, drawing (Specific to avoiding unwanted themes/styles for this concept).
b. Handling Image Input (Implicit Action/No Action):
    * When an image is provided with a scene, internally devise specific actions or movements for the subject(s) in the image based on the 'scene_description' and creative judgment.
    * Construct the Optimized Prompt for that scene focusing exclusively on the internally devised actions, implicitly referring to the image content. This prompt must NOT describe the visual elements of the image (subject appearance, background, composition). Assume the AI uses the image as the primary visual reference.
    * Generate a context-specific Negative Prompt for that scene focusing on unwanted actions or styles.
    * Example Internal Processing for Image Input (based on [Image of baby dragon on windowsill] + basic idea "animate this"):
        * Internal decision (Step 2.c): Devise actions like slow blinking, gentle head tilting, looking around with curiosity, subtle shifts in position.
        * Constructed Optimized Prompt (Step 2.d): The dragon in the image slowly blinks its large, wondrous eyes, then tilts its head gently, looking left and then right with curiosity, perhaps shifting slightly on the windowsill. (Describes only actions).
        * Constructed Negative Prompt (Step 2.e): standing up, flying away, breathing fire, cartoonish movement, inside the apartment, far shot, menacing look, scary

Input to process:
Use the following JSON as input:
{input_script_data}

Output format:
Return the full result in JSON format, for each scene add the following two fields:
- "optimized_prompt": <string>
- "negative_prompt": <string>

Example:
[
    {{
      "scene_number": 1,
      "scene_duration": 5,
      "scene_description": "a dragon flying",
      "optimized_prompt": "...",
      "negative_prompt": "..."
    }},
    ...
]
"""
    return prompt


def person_generation_prompt(user_prompt: str):
    return f"""
    You are tasked with creating an Imagen4-compatible prompt for generating a person image suitable for virtual clothing try-on.

    USER INPUT: {user_prompt}
    
    REQUIREMENTS TO INCORPORATE:
    
    PERSON SPECIFICATIONS:
    - If age not specified: adult (25-35 years old)
    - If ethnicity/skin color not specified: diverse, natural skin tone
    - If hair not specified: neat, well-styled hair (medium length)
    - If gender not specified: gender-neutral appearance
    - If body type not specified: average build, fit appearance
    - Natural, pleasant facial expression
    - Clear facial features, good bone structure
    
    POSE & POSITIONING (if not specified by user):
    - Standing straight, facing directly forward
    - Full body shot from head to feet
    - Arms relaxed at sides or slightly away from body
    - Feet shoulder-width apart, balanced stance
    - Body centered in frame
    - No tilted poses unless specifically requested by user
    
    CLOTHING (if not specified by user):
    - Simple t-shirt or basic shirt (solid colors like white, black, navy, gray)
    - Classic jeans or simple pants/trousers
    - Well-fitted, clean, wrinkle-free
    - No complex patterns, logos, or designs
    - Stick to basic casual wear only
    
    BACKGROUND & LIGHTING (if not specified by user):
    - Clean, minimalist background
    - Professional studio lighting
    - Even lighting across entire body
    - No shadows on clothing areas
    - No distracting background elements
    
    TECHNICAL REQUIREMENTS (if not specified by user):
    - Professional fashion photography style
    - High resolution, sharp focus
    - Full body portrait orientation (3:4 aspect ratio)
    - Person as main subject, clearly visible
    - Suitable for garment overlay technology
    - Clean composition, uncluttered
    
    INSTRUCTIONS:
    Generate a concise, Imagen4-compatible prompt that combines the user input with the above requirements. Follow Imagen4 prompting best practices:
    - Use clear, descriptive language
    - Be specific about visual elements
    - Keep it focused and not overly verbose
    - Include technical photography terms
    - Prioritize clarity over creativity
    
    Output only the final Imagen4 prompt, nothing else.
    """


def ad_idea_generation(ad_details_input):
    return f"""
    You are an expert creative director and ad concept artist. 
    I will give you a single input string containing a product (and possibly some direction or details). 
    Your task is to generate a single-paragraph ad idea that is highly **creative**, **unorthodox**, and **visually striking**.
    
    Do **not** generate a dull or standard ad. Avoid generic product showcases, slow pacing, or disconnected random scenes. 
    Instead, think like an indie filmmaker, anime creator, meme-maker, or bold visual storyteller. 
    The ad idea can be funny, emotional, surreal, animated, stylized, absurd, or genre-bending — but must feel **fresh**, **engaging**, and **entertaining**.
    Don’t write scene-by-scene breakdowns. Just a vivid paragraph describing the **core idea of the ad**, its vibe and concept. 
    Prioritize energy, originality, and memorability.
    
    Here’s the input string:
    {ad_details_input}
"""


def scene_prompt_generation(ad_concept):
    return f"""
    You are an expert creative director and AI prompt engineer specializing in generative video. Your task is to take a single-paragraph ad concept and transform it into a series of hyper-realistic, complex, and continuous scene prompts suitable for Google's Veo video generation model. You will adhere to the following strict rules:
    
    **Your instructions are as follows:**
    
    1.  **Deconstruct the Narrative:** First, break down the provided ad idea into a logical sequence of distinct scenes. Each scene must be designed to be a maximum of 8 seconds long and should flow seamlessly into the next.
    
    2.  **Craft Complex, Layered Prompts:** For each scene, you will write a single, comprehensive paragraph that serves as the prompt. This paragraph must be rich with detail, weaving together multiple layers of instruction to create a cinematic and evocative result. Combine the following elements into a single narrative description for each scene:
          * **Subject(s):** Describe the characters in detail, including their appearance, age, ethnicity, clothing (specify textures and style), and their specific emotional state and micro-expressions. Ensure character consistency across all scenes.
          * **Context:** Paint a vivid picture of the environment. Describe the location, time of day, weather, and specific objects. Think about what makes the setting unique.
          * **Action:** Detail the specific actions of the subjects, including subtle gestures and interactions between them or with their environment.
          * **Cinematic Style:** Define the visual aesthetic with precision. Reference specific film genres, directors (e.g., "in the style of Wes Anderson," "with the gritty realism of Denis Villeneuve"), or photographic techniques (e.g., "shot on 35mm film," "anamorphic lens flare," "Dutch angle").
          * **Camera Direction:** Specify the camera's framing (e.g., "extreme close-up," "wide shot") and any movement (e.g., "a slow dolly zoom," "a frantic handheld tracking shot").
          * **Ambiance & Lighting:** Describe the mood through lighting and color. Use evocative terms like "melancholic twilight," "warm golden hour light," "harsh neon glow," or "soft, diffused morning light." Specify the dominant color palette.

    3.  **Mandate for Specificity: Assume the Model is Blind.** This is the most important rule. The generative model has no imagination. It cannot assume details. Vague terms are forbidden. You must be relentlessly specific.
          * **DO NOT USE** ambiguous phrases like "a ball of some color," "a building of some shape," or "a normal car."
          * **YOU MUST USE** concrete, fixed terminology. For example, instead of "a red ball," you must write "a glossy, crimson red playground ball, 10 inches in diameter, with a slightly worn rubber texture." Instead of "a normal car," you must write "a dented, forest green 1998 Toyota Camry with a peeling clear coat on the hood." Every element must be described with this level of precision.
    
    4.  **Rule of Strict Consistency: Replicate Key Descriptions.** If a character or a key object appears in multiple scenes, its detailed description **must be copied and pasted exactly** into every scene prompt where it appears. This creates a "master description" that ensures the model generates the exact same person or object every time. There is no memory between scenes, so this repetition is mandatory for continuity.
    
    5.  **Final Output Format:** Your final output must be a single, valid JSON array. Each object in the array represents one scene and must contain exactly two keys:
    
          * `scene_num`: The sequential number of the scene (integer).
          * `scene_prompt`: The detailed, multi-layered descriptive paragraph for the scene (string).
    
    Input Ad Concept:
    ```{ad_concept}```
"""


def product_showcase_imagen_and_veo_prompt():
    return """
You are a generative AI that analyzes a product image and produces two specialized prompts in JSON:  
- **"imagen_prompt"**: for generating ONLY a clean background scene (without the product) that will complement the product when composited together
- **"veo_prompt"**: for animating the final composed image (background + product) in a short product showcase video (5–8s, Veo-3 style)

## Important Context:
- **INPUT**: You receive an image containing a product
- **IMAGEN OUTPUT**: Background scene only (product will be composited later)
- **VEO INPUT**: The composed image (generated background + original product)
- **VEO OUTPUT**: Animated product showcase video

## Steps:

### 1. Product Analysis
Analyze the input product image and describe:
- **Product type** (e.g., t-shirt, phone, shoe, perfume bottle, electronics)
- **Color palette** (primary, secondary, accent colors)
- **Material properties** (glossy, matte, transparent, metallic, fabric, leather, plastic)
- **Shape and form** (geometric, organic, angular, curved)
- **Texture details** (smooth, rough, ribbed, embossed, patterned)
- **Style cues** (modern, vintage, luxury, minimalist, industrial)
- **Size and scale** (relative dimensions, proportions)

### 2. Imagen Prompt Guidelines & Best Practices

**PURPOSE**: Generate ONLY the background scene (no product) that will complement the product when composited

**Core Structure:**
```
[BACKGROUND ENVIRONMENT] + [LIGHTING SETUP] + [SURFACE/PLATFORM] + [COMPOSITION SPACE] + [STYLE] + [CAMERA] + [QUALITY]
```

**Essential Elements:**
- **Background Environment**: 
  - Setting type (studio backdrop, natural environment, architectural space)
  - Surface/platform for product placement (table, pedestal, floating platform, ground)
  - Environmental elements (walls, horizon, architectural details)
  - Spatial depth and layers
- **Lighting Setup**:
  - Key light direction and quality (soft studio lighting, natural window light)
  - Fill lighting to eliminate harsh shadows
  - Accent/rim lighting positions
  - Color temperature (warm tungsten, cool daylight, neutral)
- **Surface & Platform Details**:
  - Material (marble, wood, metal, glass, fabric)
  - Texture (smooth, rough, reflective, matte)
  - Color that complements product
  - Size and proportion for product placement
- **Composition Space**:
  - Empty space reserved for product placement
  - Rule of thirds grid consideration
  - Leading lines directing to product area
  - Negative space balance
- **Style Parameters**:
  - Photorealistic studio photography
  - Commercial product photography aesthetic
  - Color grading that enhances product colors
- **Camera Settings**:
  - Lens type (85mm portrait, 50mm standard)
  - Depth of field (shallow to blur background, deep for context)
  - Perspective height (eye-level, slightly elevated)
- **Quality Modifiers**: "high resolution," "professional product photography," "commercial studio quality"

**Advanced Techniques:**
- **Complementary Colors**: Choose background colors that make product pop
- **Material Contrast**: Juxtapose different textures (smooth product on rough surface)
- **Atmospheric Depth**: Subtle gradients, soft shadows for dimension
- **Brand Alignment**: Luxury, minimal, industrial, or organic aesthetic
- **Contextual Relevance**: Environment that tells product story without distraction


### 3. Veo-3 Prompt Guidelines & Best Practices

**PURPOSE**: Animate the final composed image (background + product) for a compelling product showcase

**Core Structure:**
```
[COMPOSED SCENE SETUP] + [CAMERA MOVEMENT] + [LIGHTING CHANGES] + [PRODUCT INTERACTION] + [DURATION/PACING] + [AUDIO/ATMOSPHERE]
```

**Essential Elements:**

**Composed Scene Description:**
- Describe the product positioned in the generated background
- Initial state: "Product elegantly placed on [surface] in [environment]"
- Spatial relationships between product and background elements
- Overall composition and framing

**Camera Movement (Choose 1-2 max):**
- **Dolly**: "slow dolly in toward product," "smooth dolly out revealing full scene"
- **Pan**: "gentle pan right showcasing product," "sweeping pan across composition"
- **Tilt**: "subtle tilt up revealing product majesty," "dramatic tilt down to product"
- **Zoom**: "slow zoom in highlighting product details," "gradual zoom out for context"
- **Orbit**: "circular orbit around product," "partial orbit revealing product angles"
- **Track**: "tracking shot following product form," "smooth lateral tracking"

**Lighting Dynamics:**
- **Transitions**: "lighting gradually brightens on product," "shadows shift across background"
- **Product Highlighting**: "spotlight sweeps across product surface," "rim lighting emerges around product edges"
- **Reflections**: "light catches product material," "subtle reflections appear on surface"
- **Color shifts**: "warm to cool transition," "golden hour effect on scene"

**Product Interaction:**
- **Subtle movements**: "product gently rotates," "slight floating motion," "elegant sway"
- **Reveal techniques**: "product emerges from soft shadow," "focus pulls to product details"
- **Material showcase**: "light reveals product texture," "surface catches and reflects light"
- **Scale emphasis**: "camera reveals product proportions," "close-up details then wide shot"

**Pacing & Duration:**
- **Timing**: "5-second sequence," "8-second duration"
- **Rhythm**: "slow and steady reveal," "gradual acceleration," "smooth deceleration"
- **Keyframes**: "starts with wide shot... transitions to close-up... ends with hero angle"

**Audio & Atmosphere:**
- **Ambient sound**: "soft atmospheric hum," "gentle whoosh," "studio ambiance"
- **Product sounds**: "subtle swoosh during rotation," "gentle chime," "soft material sounds"
- **Musical elements**: "ethereal tones," "modern beat," "luxury ambiance"

**Advanced Veo-3 Techniques:**

**Cinematography:**
- **Shot progression**: "establishing shot of scene," "product close-up," "macro detail," "final hero shot"
- **Lens effects**: "shallow focus on product," "deep focus for context," "bokeh," "lens flare"
- **Framing**: "product as hero subject," "background as supporting element"
- **Composition**: "rule of thirds with product," "leading lines to product," "symmetrical framing"

**Visual Effects:**
- **Particle systems**: "floating particles around product," "light rays," "sparkles"
- **Atmospheric effects**: "mist," "smoke," "light beams enhancing product"
- **Transitions**: "fade in/out," "dissolve," "wipe"

**Emotional Storytelling:**
- **Mood**: "aspirational," "premium," "accessible," "innovative"
- **Narrative arc**: Product introduction → feature highlight → final impression
- **Brand personality**: Luxury, playful, professional, cutting-edge

**Technical Specifications:**
- **Resolution**: "4K quality," "high definition"
- **Frame rate**: "smooth 24fps," "cinematic 30fps"
- **Color grading**: "commercial grade," "film-like," "vibrant"

**Common Pitfalls to Avoid:**
- Don't use instructive language ("don't show," "avoid")
- Avoid over-complicating with too many simultaneous movements
- Don't specify exact timing beyond 5-8 seconds
- Avoid contradictory camera movements
- Don't over-describe static elements

**Best Practices:**
- Use "this then that" sequential structure for complex actions
- Be specific about camera positioning and movement speed
- Include atmospheric and audio elements for immersion
- Specify the emotional tone and brand feeling
- Use cinematic terminology for professional results
- Test with shorter, simpler prompts first

## 4. Output Format

Return exactly valid JSON with keys:  
```json
{
  "imagen_prompt": "Background generation prompt (NO product, only environment/setting that will complement the product)",
  "veo_prompt": "Video animation prompt (assumes product is composited on the generated background)"
}
```
    """
