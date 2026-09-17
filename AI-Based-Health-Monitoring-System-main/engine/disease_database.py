"""
Clinical Disease Database
Comprehensive repository of 40+ medical conditions with symptom profiles,
clinical weights, severity classifications, and home care recommendations.
"""

DISEASE_DATABASE = {
    # ==================== INFECTIOUS DISEASES ====================
    "dengue": {
        "name": "Dengue Fever",
        "category": "Infectious Diseases",
        "severity": "high",
        "primary_symptoms": ["high_fever", "severe_headache", "pain_behind_eyes", "joint_pain", "muscle_pain", "skin_rash"],
        "secondary_symptoms": ["nausea", "vomiting", "fatigue", "mild_bleeding", "loss_of_appetite"],
        "red_flags": ["Severe abdominal pain", "Persistent vomiting", "Bleeding gums or nose", "Extreme lethargy", "Blood in vomit/stool"],
        "description": "A mosquito-borne viral infection causing sudden high fever, intense joint and muscle pain ('breakbone fever'), retro-orbital pain, and rash.",
        "home_care": [
            "Maintain strict hydration with ORS, coconut water, fruit juices, and clear soups.",
            "Complete physical bed rest to conserve platelet reserves.",
            "Use paracetamol for fever and pain. STRICTLY AVOID aspirin, ibuprofen, or naproxen (increases bleeding risk).",
            "Monitor platelet counts daily via complete blood count (CBC)."
        ],
        "medications_otc": "Paracetamol (500-650 mg every 6 hours for adults). No NSAIDs.",
        "when_to_see_doctor": "Immediately if signs of bleeding, severe abdominal pain, breathlessness, or persistent vomiting appear."
    },
    "malaria": {
        "name": "Malaria",
        "category": "Infectious Diseases",
        "severity": "high",
        "primary_symptoms": ["chills", "high_fever", "sweating", "shivering", "headache"],
        "secondary_symptoms": ["nausea", "vomiting", "body_ache", "fatigue", "diarrhea", "anemia"],
        "red_flags": ["Confusion or delirium", "Severe breathlessness", "Yellowish eyes/skin (jaundice)", "Dark or tea-colored urine"],
        "description": "A life-threatening disease caused by Plasmodium parasites transmitted through infected Anopheles mosquito bites, marked by cyclical fever episodes.",
        "home_care": [
            "Seek formal blood smear (microscopy) or rapid diagnostic test (RDT) urgently.",
            "Drink plenty of fluids with electrolytes to replace fluid lost from sweating.",
            "Rest in a cool room; lukewarm sponging during high fever spikes."
        ],
        "medications_otc": "Antimalarials require prescription (e.g. Artemisinin-based combinations). Paracetamol for fever.",
        "when_to_see_doctor": "Consult a doctor within 24 hours of suspected symptoms for blood testing and targeted prescription antimalarials."
    },
    "typhoid": {
        "name": "Typhoid Fever",
        "category": "Infectious Diseases",
        "severity": "high",
        "primary_symptoms": ["prolonged_fever", "stomach_pain", "headache", "extreme_fatigue", "loss_of_appetite"],
        "secondary_symptoms": ["constipation_or_diarrhea", "rose_spots", "dry_cough", "nausea", "swollen_abdomen"],
        "red_flags": ["Severe abdominal rigidity", "Internal bleeding", "Confusion", "Persistent high step-ladder fever (>103°F)"],
        "description": "A systemic bacterial infection caused by Salmonella Typhi, spread through contaminated food and water.",
        "home_care": [
            "Consume only boiled, bottled, or purified water; eat thoroughly cooked, easily digestible foods.",
            "Avoid raw vegetables, unpeeled fruits, and street food.",
            "Maintain strict hand hygiene after using the restroom."
        ],
        "medications_otc": "Requires prescription antibiotics (e.g. Ceftriaxone, Azithromycin). Oral rehydration salts (ORS).",
        "when_to_see_doctor": "Prompt clinical evaluation required. Widal test or blood culture needed."
    },
    "covid_19": {
        "name": "COVID-19 (Coronavirus)",
        "category": "Infectious Diseases",
        "severity": "moderate",
        "primary_symptoms": ["fever", "dry_cough", "loss_of_taste_smell", "fatigue", "sore_throat"],
        "secondary_symptoms": ["shortness_of_breath", "body_ache", "headache", "nasal_congestion", "diarrhea"],
        "red_flags": ["Oxygen saturation (SpO2) < 94%", "Persistent chest pressure", "Confusion", "Bluish lips/face"],
        "description": "A contagious respiratory infection caused by SARS-CoV-2, ranging from mild cold-like symptoms to viral pneumonia.",
        "home_care": [
            "Isolate in a well-ventilated room to prevent transmission.",
            "Monitor SpO2 with a pulse oximeter every 4-6 hours.",
            "Warm saline gargles and steam inhalation for throat relief.",
            "Generous hydration and balanced, protein-rich nutrition."
        ],
        "medications_otc": "Paracetamol for fever, saline nasal spray, cough lozenges.",
        "when_to_see_doctor": "Seek emergency care if SpO2 drops below 94% or severe breathing difficulty occurs."
    },
    "influenza": {
        "name": "Influenza (Flu)",
        "category": "Infectious Diseases",
        "severity": "moderate",
        "primary_symptoms": ["sudden_high_fever", "severe_body_ache", "dry_cough", "fatigue", "chills"],
        "secondary_symptoms": ["headache", "sore_throat", "runny_nose", "dizziness"],
        "red_flags": ["Difficulty breathing", "Chest pain", "Persistent dizziness", "Fever returning after improvement"],
        "description": "An acute viral respiratory infection causing rapid onset of systemic symptoms including high fever and severe muscle aches.",
        "home_care": [
            "Complete rest for at least 5-7 days.",
            "Drink hot broths, herbal teas, and water to loosen respiratory secretions.",
            "Use a room humidifier to soothe irritated airways."
        ],
        "medications_otc": "Acetaminophen/Paracetamol or Ibuprofen (adults only), warm throat lozenges.",
        "when_to_see_doctor": "If fever persists past 4 days, breathing becomes difficult, or for high-risk patients (seniors, pregnant women)."
    },
    "common_cold": {
        "name": "Common Cold (Viral Rhinitis)",
        "category": "Infectious Diseases",
        "severity": "mild",
        "primary_symptoms": ["runny_nose", "nasal_congestion", "sneezing", "sore_throat"],
        "secondary_symptoms": ["mild_cough", "low_fever", "mild_headache", "watery_eyes"],
        "red_flags": ["Earache with fever", "Symptoms worsening after 10 days", "High fever > 101.5°F"],
        "description": "A mild viral infection of the upper respiratory tract primarily affecting the nose and throat.",
        "home_care": [
            "Stay warm, well-hydrated, and well-rested.",
            "Steam inhalation with eucalyptus or plain water.",
            "Warm salt water gargles 3 times a day."
        ],
        "medications_otc": "Saline nasal drops, antihistamines for sneezing, lozenges for throat irritation.",
        "when_to_see_doctor": "If symptoms do not improve within 10-14 days or secondary bacterial sinusitis develops."
    },
    "hepatitis_jaundice": {
        "name": "Acute Viral Hepatitis / Jaundice",
        "category": "Infectious Diseases",
        "severity": "high",
        "primary_symptoms": ["yellow_eyes_skin", "dark_urine", "pale_stools", "loss_of_appetite", "fatigue"],
        "secondary_symptoms": ["nausea", "vomiting", "mild_fever", "right_upper_abdominal_pain", "itching"],
        "red_flags": ["Altered mental state or confusion", "Severe persistent vomiting", "Spontaneous bleeding or bruising"],
        "description": "Inflammation of the liver caused by viral pathogens (Hepatitis A/B/C/E), impairing bilirubin metabolism and liver enzymes.",
        "home_care": [
            "Strictly avoid alcohol and hepatotoxic substances.",
            "Eat a low-fat, high-carbohydrate, easily digestible diet (fruits, sugarcane juice, boiled grains).",
            "Rest adequately and avoid strenuous physical exertion."
        ],
        "medications_otc": "Do NOT take unprescribed painkillers or acetaminophen without doctor guidance (liver stress).",
        "when_to_see_doctor": "Urgent liver function test (LFT) and ultrasound abdomen required."
    },
    "tuberculosis": {
        "name": "Pulmonary Tuberculosis (TB)",
        "category": "Infectious Diseases",
        "severity": "high",
        "primary_symptoms": ["chronic_cough", "coughing_blood", "night_sweats", "unexplained_weight_loss", "low_fever"],
        "secondary_symptoms": ["fatigue", "chest_pain_with_breathing", "loss_of_appetite", "breathlessness"],
        "red_flags": ["Massive hemoptysis (coughing up large amounts of blood)", "Severe chest pain", "Marked emaciation"],
        "description": "A serious chronic bacterial infection caused by Mycobacterium tuberculosis, primarily attacking the lungs.",
        "home_care": [
            "Strict adherence to prescribed DOTS (Directly Observed Therapy) antibiotic regimen without missing a single dose.",
            "Maintain high-protein diet to rebuild strength.",
            "Wear masks and maintain good room ventilation to protect family members."
        ],
        "medications_otc": "Requires prescription multi-drug anti-TB regimen (Rifampicin, Isoniazid, Pyrazinamide, Ethambutol).",
        "when_to_see_doctor": "Immediate chest X-ray and sputum testing required."
    },

    # ==================== RESPIRATORY DISEASES ====================
    "pneumonia": {
        "name": "Pneumonia",
        "category": "Respiratory Diseases",
        "severity": "critical",
        "primary_symptoms": ["high_fever", "productive_cough_with_colored_phlegm", "shortness_of_breath", "sharp_chest_pain_on_breathing"],
        "secondary_symptoms": ["chills", "sweating", "fatigue", "confusion_in_elderly", "rapid_shallow_breathing"],
        "red_flags": ["SpO2 < 93%", "Blue lips or nail beds", "Severe chest pain on inhaling", "Lethargy/confusion in seniors"],
        "description": "An infection that inflames the air sacs (alveoli) in one or both lungs, which may fill with fluid or purulent material.",
        "home_care": [
            "Requires immediate professional medical evaluation.",
            "Elevate head on pillows to ease breathing.",
            "Monitor oxygen levels closely with a pulse oximeter."
        ],
        "medications_otc": "Antibiotics or antivirals must be prescribed by a physician.",
        "when_to_see_doctor": "Seek emergency medical care immediately. Do not delay."
    },
    "asthma": {
        "name": "Bronchial Asthma / Asthma Exacerbation",
        "category": "Respiratory Diseases",
        "severity": "high",
        "primary_symptoms": ["wheezing", "shortness_of_breath", "chest_tightness", "chronic_cough_especially_night"],
        "secondary_symptoms": ["difficulty_speaking_in_sentences", "anxiety", "rapid_breathing", "fatigue"],
        "red_flags": ["Severe struggle for breath", "Inhaler provides no relief", "Ribs sucking in during breaths (retractions)", "Bluish tint around lips"],
        "description": "A chronic inflammatory airway condition where bronchial tubes narrow, swell, and produce excess mucus in response to triggers.",
        "home_care": [
            "Use rescue bronchodilator inhaler (e.g. Salbutamol / Albuterol) immediately via spacer as per your action plan.",
            "Sit upright; do NOT lie flat.",
            "Move away from smoke, dust, cold air, or pet dander triggers.",
            "Practice pursed-lip breathing to slow respiratory rate."
        ],
        "medications_otc": "Prescribed reliever inhalers (Salbutamol). Avoid beta-blockers and aspirin.",
        "when_to_see_doctor": "If rescue inhaler doesn't bring relief within 15 minutes, proceed to emergency room."
    },
    "bronchitis": {
        "name": "Acute Bronchitis",
        "category": "Respiratory Diseases",
        "severity": "moderate",
        "primary_symptoms": ["persistent_cough_with_mucus", "chest_discomfort", "fatigue", "mild_fever"],
        "secondary_symptoms": ["sore_throat", "shortness_of_breath_on_exertion", "wheezing", "body_ache"],
        "red_flags": ["Coughing blood", "Fever > 102°F", "Shortness of breath at rest", "Symptoms lasting > 3 weeks"],
        "description": "Inflammation of the lining of the bronchial tubes, commonly following a viral respiratory illness.",
        "home_care": [
            "Drink warm fluids and teas to thin bronchial mucus.",
            "Inhale steam twice daily.",
            "Avoid secondhand smoke and chemical fumes.",
            "Rest voice and body."
        ],
        "medications_otc": "Expectorant cough syrups (guaifenesin), honey (for individuals > 1 year), paracetamol.",
        "when_to_see_doctor": "If cough produces blood or persists for more than 3 weeks."
    },
    "sinusitis": {
        "name": "Acute / Chronic Sinusitis",
        "category": "Respiratory Diseases",
        "severity": "mild",
        "primary_symptoms": ["facial_pain_pressure", "nasal_blockage", "thick_yellow_green_discharge", "headache_worse_bending_forward"],
        "secondary_symptoms": ["reduced_sense_of_smell", "tooth_pain_upper_jaw", "bad_breath", "fatigue", "ear_fullness"],
        "red_flags": ["Swelling or redness around eyes", "Double vision", "Severe stiff neck", "High fever with confusion"],
        "description": "Inflammation or infection of the tissue lining the paranasal sinuses, blocking mucus drainage.",
        "home_care": [
            "Warm facial compress over nose, cheeks, and eyes.",
            "Saline nasal rinses (neti pot or spray) twice daily.",
            "Stay well-hydrated and breathe in warm steam."
        ],
        "medications_otc": "Saline nasal spray, oral decongestants (short term max 3 days), paracetamol for pain.",
        "when_to_see_doctor": "If symptoms last > 10 days without improvement or facial swelling occurs."
    },

    # ==================== CARDIOVASCULAR DISEASES ====================
    "hypertension": {
        "name": "Hypertension (High Blood Pressure)",
        "category": "Cardiovascular Diseases",
        "severity": "moderate",
        "primary_symptoms": ["occipital_headache_morning", "dizziness", "blurred_vision", "palpitations"],
        "secondary_symptoms": ["facial_flushing", "fatigue", "nosebleeds", "shortness_of_breath"],
        "red_flags": ["Systolic BP > 180 or Diastolic > 120 (Hypertensive Crisis)", "Chest pain", "Numbness/weakness", "Speech difficulty"],
        "description": "A long-term condition where blood exerts persistently elevated arterial pressure, taxing the heart and blood vessels.",
        "home_care": [
            "Adopt the DASH diet: reduce dietary sodium to < 1500mg/day, increase potassium-rich greens.",
            "Engage in 30 minutes of moderate aerobic activity daily (walking, cycling).",
            "Avoid tobacco, limit caffeine and alcohol, practice stress reduction."
        ],
        "medications_otc": "Antihypertensive medications (ACE inhibitors, ARBs, CCBs) require physician prescription.",
        "when_to_see_doctor": "Routine BP checks recommended. Seek immediate ER care if BP exceeds 180/120 with headache or chest discomfort."
    },
    "angina_coronary": {
        "name": "Angina Pectoris / Suspected Acute Coronary Syndrome",
        "category": "Cardiovascular Diseases",
        "severity": "critical",
        "primary_symptoms": ["chest_pressure_squeezing", "pain_radiating_to_arm_neck_jaw", "shortness_of_breath", "cold_sweating"],
        "secondary_symptoms": ["nausea", "lightheadedness", "palpitations", "anxiety"],
        "red_flags": ["Chest pain lasting > 5 minutes", "Pain not relieved by rest", "Profuse cold sweat with fainting"],
        "description": "Chest pain caused by reduced blood flow to cardiac muscle. An urgent warning sign of potential myocardial infarction (heart attack).",
        "home_care": [
            "CALL EMERGENCY SERVICES (911 / 108 / 112) IMMEDIATELY.",
            "Sit upright and rest completely. Do NOT walk or exert yourself.",
            "If prescribed, take sublingual Nitroglycerin.",
            "Chew one 300mg uncoated Aspirin unless allergic or contraindicated."
        ],
        "medications_otc": "Chewable Aspirin (emergency first-aid only). Emergency medical evaluation mandatory.",
        "when_to_see_doctor": "IMMEDIATE EMERGENCY ROOM VISIT REQUIRED. Call an ambulance."
    },
    "cardiac_arrhythmia": {
        "name": "Cardiac Arrhythmia / Tachycardia",
        "category": "Cardiovascular Diseases",
        "severity": "high",
        "primary_symptoms": ["palpitations_racing_heart", "skipped_heartbeats", "dizziness", "shortness_of_breath"],
        "secondary_symptoms": ["chest_fluttering", "fatigue", "near_fainting", "lightheadedness"],
        "red_flags": ["Complete fainting (syncope)", "Chest pain with racing pulse", "Shortness of breath at rest"],
        "description": "An improper beating of the heart, whether irregular, too fast (tachycardia > 100 bpm), or too slow (bradycardia < 60 bpm).",
        "home_care": [
            "Sit or lie down immediately when palpitations occur.",
            "Avoid stimulants: caffeine, energy drinks, nicotine, and decongestants.",
            "Perform vagal maneuvers (e.g. bearing down or splashing cold water on face) if instructed by doctor."
        ],
        "medications_otc": "No OTC antiarrhythmics. Prescription required after ECG / Holter monitoring.",
        "when_to_see_doctor": "Schedule a cardiology consultation with 12-lead ECG."
    },

    # ==================== GASTROINTESTINAL DISEASES ====================
    "gastroenteritis": {
        "name": "Acute Gastroenteritis / Food Poisoning",
        "category": "Gastrointestinal Diseases",
        "severity": "moderate",
        "primary_symptoms": ["watery_diarrhea", "vomiting", "abdominal_cramps", "nausea"],
        "secondary_symptoms": ["low_fever", "headache", "dehydration_thirst", "loss_of_appetite"],
        "red_flags": ["Inability to keep liquids down for 12+ hours", "Blood in stool or vomit", "High fever > 102°F", "Sunken eyes, no urination"],
        "description": "Inflammation of the stomach and intestines typically caused by bacterial, viral, or parasite-contaminated food or water.",
        "home_care": [
            "Rehydrate vigorously: sip Oral Rehydration Solution (ORS) every 10-15 minutes.",
            "Transition slowly to the BRAT diet: Bananas, Rice, Applesauce, Toast.",
            "Avoid dairy, spicy food, caffeine, and greasy meals for 48 hours."
        ],
        "medications_otc": "ORS packets, Zinc supplements (for children), Probiotics. Avoid anti-diarrheals if fever/blood present.",
        "when_to_see_doctor": "If signs of severe dehydration, blood in stool, or vomiting persists over 24 hours."
    },
    "gerd_acid_reflux": {
        "name": "GERD (Gastroesophageal Reflux Disease)",
        "category": "Gastrointestinal Diseases",
        "severity": "mild",
        "primary_symptoms": ["heartburn_burning_chest", "acid_regurgitation", "sour_taste_in_mouth", "upper_abdominal_discomfort"],
        "secondary_symptoms": ["chronic_dry_cough", "globus_sensation_lump_in_throat", "difficulty_swallowing", "bloating"],
        "red_flags": ["Difficulty or pain when swallowing (dysphagia)", "Unexplained weight loss", "Black tarry stools", "Vomiting blood"],
        "description": "A chronic digestive condition where stomach acid or bile irritates the lining of the food pipe (esophagus).",
        "home_care": [
            "Eat smaller, more frequent meals; avoid lying down within 3 hours after eating.",
            "Elevate the head of your bed by 6 inches with risers.",
            "Avoid trigger foods: citrus, tomatoes, chocolate, caffeine, mint, fatty fried dishes.",
            "Maintain a healthy body weight to reduce intra-abdominal pressure."
        ],
        "medications_otc": "Antacids (magnesium/aluminum hydroxide), H2 blockers (famotidine), or PPIs (omeprazole).",
        "when_to_see_doctor": "If symptoms occur more than twice weekly or if dysphagia occurs."
    },
    "peptic_ulcer": {
        "name": "Peptic Ulcer Disease",
        "category": "Gastrointestinal Diseases",
        "severity": "high",
        "primary_symptoms": ["burning_stomach_pain_between_meals", "bloating", "nausea", "feeling_full_too_soon"],
        "secondary_symptoms": ["heartburn", "intolerance_to_fatty_foods", "belching", "weight_loss"],
        "red_flags": ["Vomiting blood or coffee-ground material", "Dark, tarry, foul-smelling stools", "Sudden sharp piercing abdominal pain"],
        "description": "Sores that develop on the inside lining of the stomach (gastric ulcer) or the upper small intestine (duodenal ulcer), commonly linked to H. pylori or NSAIDs.",
        "home_care": [
            "Avoid NSAID painkillers (ibuprofen, naproxen, aspirin) which directly erode stomach mucosa.",
            "Stop smoking and avoid alcohol.",
            "Eat soothing foods: yogurt, oats, steamed vegetables."
        ],
        "medications_otc": "Antacids for temporary relief. Requires prescription H. pylori eradication therapy.",
        "when_to_see_doctor": "Endoscopic evaluation recommended if symptoms persist or dark stools appear."
    },
    "appendicitis": {
        "name": "Acute Appendicitis",
        "category": "Gastrointestinal Diseases",
        "severity": "critical",
        "primary_symptoms": ["sudden_pain_lower_right_abdomen", "pain_worse_with_coughing_walking", "nausea", "vomiting", "low_fever"],
        "secondary_symptoms": ["loss_of_appetite", "constipation_or_diarrhea", "abdominal_swelling"],
        "red_flags": ["Pain starting near belly button and shifting to right lower abdomen", "Abdominal rigidity", "Rebound tenderness"],
        "description": "A medical emergency involving acute inflammation of the appendix, with risk of rupture and peritonitis.",
        "home_care": [
            "DO NOT apply heating pads, take enemas, or take laxatives (increases rupture risk).",
            "Do NOT eat or drink in anticipation of emergency surgery.",
            "Go to the emergency department immediately."
        ],
        "medications_otc": "DO NOT take pain relievers before clinical examination as it masks peritoneal signs.",
        "when_to_see_doctor": "IMMEDIATE EMERGENCY ROOM VISIT. Surgical emergency."
    },
    "ibs": {
        "name": "Irritable Bowel Syndrome (IBS)",
        "category": "Gastrointestinal Diseases",
        "severity": "mild",
        "primary_symptoms": ["cramping_abdominal_pain_relieved_by_defecation", "bloating", "alternating_diarrhea_constipation"],
        "secondary_symptoms": ["excess_gas", "mucus_in_stool", "feeling_incomplete_evacuation", "fatigue"],
        "red_flags": ["Unexplained weight loss", "Onset after age 50", "Rectal bleeding", "Nocturnal diarrhea waking from sleep"],
        "description": "A common functional gastrointestinal disorder affecting the large intestine with altered gut motility and hypersensitivity.",
        "home_care": [
            "Follow a Low-FODMAP diet under nutritional guidance.",
            "Gradually increase soluble fiber (psyllium husk).",
            "Engage in stress reduction: yoga, mindfulness, regular exercise.",
            "Keep a food symptom diary to identify individual triggers."
        ],
        "medications_otc": "Probiotics, peppermint oil capsules, antispasmodics.",
        "when_to_see_doctor": "Consult gastroenterologist for diagnosis and exclusion of inflammatory bowel disease."
    },

    # ==================== ENDOCRINE & METABOLIC ====================
    "diabetes_mellitus": {
        "name": "Type 2 Diabetes Mellitus",
        "category": "Endocrine & Metabolic Diseases",
        "severity": "high",
        "primary_symptoms": ["frequent_urination", "excessive_thirst", "unexplained_weight_loss", "increased_hunger", "extreme_fatigue"],
        "secondary_symptoms": ["blurry_vision", "slow_healing_sores", "frequent_infections", "tingling_numbness_hands_feet"],
        "red_flags": ["Fruity breath odor", "Extreme confusion", "Rapid deep breathing (Kussmaul breathing)", "Blood glucose > 300 mg/dL"],
        "description": "A chronic metabolic condition characterized by insulin resistance and elevated blood glucose levels, leading to microvascular and macrovascular complications.",
        "home_care": [
            "Adopt a low-glycemic index, high-fiber, balanced diabetic meal plan.",
            "Exercise 30-45 minutes at least 5 days a week to improve insulin sensitivity.",
            "Daily foot inspections for small cuts, blisters, or calluses.",
            "Maintain a daily log of fasting and postprandial blood sugar readings."
        ],
        "medications_otc": "Requires prescription antidiabetic medication (Metformin, SGLT2 inhibitors) or insulin.",
        "when_to_see_doctor": "HbA1c test and comprehensive diabetic workup required."
    },
    "hypothyroidism": {
        "name": "Hypothyroidism (Underactive Thyroid)",
        "category": "Endocrine & Metabolic Diseases",
        "severity": "moderate",
        "primary_symptoms": ["unexplained_weight_gain", "cold_intolerance", "chronic_fatigue", "dry_skin", "constipation"],
        "secondary_symptoms": ["hair_thinning", "puffy_face", "muscle_weakness", "slow_heart_rate", "mood_depression"],
        "red_flags": ["Severe hypothermia", "Extreme confusion or stupor (Myxedema coma)"],
        "description": "A condition where the thyroid gland does not produce sufficient thyroid hormones (T3/T4), slowing metabolism.",
        "home_care": [
            "Take prescribed levothyroxine consistently in the morning on an empty stomach with water.",
            "Wait at least 30-60 minutes before breakfast or coffee.",
            "Ensure adequate dietary iodine and selenium from balanced foods."
        ],
        "medications_otc": "Prescription Levothyroxine is the standard therapy. No OTC thyroid pills.",
        "when_to_see_doctor": "Serum TSH, Free T3, and Free T4 blood testing."
    },
    "hyperthyroidism": {
        "name": "Hyperthyroidism (Overactive Thyroid)",
        "category": "Endocrine & Metabolic Diseases",
        "severity": "high",
        "primary_symptoms": ["unexplained_weight_loss_despite_eating", "rapid_heartbeat_palpitations", "heat_intolerance", "nervousness_tremors"],
        "secondary_symptoms": ["increased_appetite", "sweating", "frequent_bowel_movements", "sleep_disturbances", "bulging_eyes"],
        "red_flags": ["High fever, extreme agitation, heart rate > 140 bpm (Thyroid Storm emergency)"],
        "description": "Excessive production of thyroid hormones resulting in a hypermetabolic state.",
        "home_care": [
            "Avoid high-iodine supplements (kelp, seaweed) until medically evaluated.",
            "Rest frequently and avoid high ambient temperatures.",
            "Protect eyes with lubricating drops if bulging/dryness is present."
        ],
        "medications_otc": "Requires prescription antithyroid agents (Methimazole) or beta-blockers.",
        "when_to_see_doctor": "Urgent endocrinology referral and thyroid panel testing."
    },

    # ==================== NEUROLOGICAL DISEASES ====================
    "migraine": {
        "name": "Migraine Headache",
        "category": "Neurological Diseases",
        "severity": "moderate",
        "primary_symptoms": ["throbbing_one_sided_headache", "sensitivity_to_light_photophobia", "sensitivity_to_sound_phonophobia", "nausea"],
        "secondary_symptoms": ["visual_aura_flashes", "vomiting", "dizziness", "neck_stiffness", "irritability"],
        "red_flags": ["Worst headache of life (Thunderclap)", "Headache with fever and stiff neck", "Sudden weakness or numbness on one side of face/body"],
        "description": "A neurological condition featuring moderate-to-severe pulsating unilateral headaches, frequently accompanied by autonomic and sensory symptoms.",
        "home_care": [
            "Rest in a completely dark, quiet room with cold compress on forehead.",
            "Hydrate with 500ml water immediately upon onset of aura or prodrome.",
            "Avoid known dietary triggers: aged cheeses, MSG, nitrates, artificial sweeteners, alcohol.",
            "Maintain regular sleep schedules and stress management."
        ],
        "medications_otc": "Ibuprofen, Naproxen, or Paracetamol taken at the first sign of headache.",
        "when_to_see_doctor": "If headaches occur > 4 times a month or fail to respond to standard medications."
    },
    "tension_headache": {
        "name": "Tension-Type Headache",
        "category": "Neurological Diseases",
        "severity": "mild",
        "primary_symptoms": ["band_like_tightness_around_head", "dull_aching_head_pain", "tenderness_neck_shoulder_scalp"],
        "secondary_symptoms": ["mild_fatigue", "difficulty_concentrating", "mild_eye_strain"],
        "red_flags": ["Sudden explosive onset", "Accompanied by loss of consciousness", "Post-trauma headache"],
        "description": "The most common form of headache, typically caused by muscle contraction and tension in the neck, scalp, and shoulders.",
        "home_care": [
            "Apply a warm heating pad or take a warm shower to relax neck muscles.",
            "Practice gentle neck and upper shoulder stretches.",
            "Take 10-minute breaks every hour from computer and mobile screens.",
            "Ensure ergonomic seating and proper hydration."
        ],
        "medications_otc": "Paracetamol, Ibuprofen, or Aspirin.",
        "when_to_see_doctor": "If chronic (occurring more than 15 days per month)."
    },
    "vertigo_bppv": {
        "name": "Vertigo (BPPV / Inner Ear Disturbance)",
        "category": "Neurological Diseases",
        "severity": "moderate",
        "primary_symptoms": ["spinning_sensation", "loss_of_balance", "dizziness_triggered_by_head_movement", "nausea"],
        "secondary_symptoms": ["vomiting", "nystagmus_abnormal_eye_movement", "ear_fullness", "lightheadedness"],
        "red_flags": ["Sudden hearing loss", "Double vision", "Slurred speech", "Focal arm/leg weakness (Stroke warning)"],
        "description": "A sensation that you or your surroundings are spinning, frequently caused by loose calcium carbonate crystals in the semicircular canals of the inner ear.",
        "home_care": [
            "Sit or lie still immediately; change positions very slowly.",
            "Avoid bending down or looking up quickly.",
            "Perform vestibular rehabilitation exercises (Epley maneuver) if diagnosed with BPPV.",
            "Ensure good room lighting to avoid fall hazards."
        ],
        "medications_otc": "Motion sickness medications (Meclizine, Dimenhydrinate) for short-term nausea.",
        "when_to_see_doctor": "ENT or neurology consultation. Emergency if associated with neurological deficits."
    },

    # ==================== DERMATOLOGICAL DISEASES ====================
    "allergic_contact_dermatitis": {
        "name": "Allergic Contact Dermatitis / Eczema",
        "category": "Dermatological Diseases",
        "severity": "mild",
        "primary_symptoms": ["intense_skin_itching", "red_rash", "dry_cracked_scaly_skin", "small_blisters"],
        "secondary_symptoms": ["skin_swelling", "burning_or_stinging_sensation", "skin_thickening_lichenification"],
        "red_flags": ["Signs of secondary bacterial infection (pus oozing, honey-colored crusts, red streaks, fever)"],
        "description": "An inflammatory skin reaction triggered by contact with allergens (nickel, soaps, cosmetics, poison ivy) or genetic atopic vulnerability.",
        "home_care": [
            "Apply rich fragrance-free emollient creams or petroleum jelly immediately after bathing.",
            "Take short, lukewarm showers (avoid hot water which dries skin).",
            "Wear loose, soft cotton clothing; avoid wool and synthetic fabrics.",
            "Use cold damp compresses to relieve active itch without scratching."
        ],
        "medications_otc": "Hydrocortisone 1% cream (short term), oral antihistamines (Cetirizine, Loratadine) for itching.",
        "when_to_see_doctor": "If rash covers large areas or displays signs of bacterial infection."
    },
    "urticaria_hives": {
        "name": "Acute Urticaria (Hives)",
        "category": "Dermatological Diseases",
        "severity": "moderate",
        "primary_symptoms": ["raised_red_itchy_welts_wheals", "itchy_skin_swelling", "welts_changing_shape_and_location"],
        "secondary_symptoms": ["angioedema_lip_eye_swelling", "mild_burning", "skin_warmth"],
        "red_flags": ["Swelling of the tongue, throat, or lips", "Wheezing or difficulty breathing", "Dizziness/anaphylaxis (CALL 911/108/112)"],
        "description": "A sudden outbreak of raised, intensely pruritic wheals triggered by histamine release in response to allergens, medications, infections, or stress.",
        "home_care": [
            "Apply cool compresses or take a cool colloidal oatmeal bath.",
            "Wear loose-fitting, soft cotton clothing.",
            "Avoid scratching, hot baths, and vigorous skin rubbing.",
            "Identify and avoid suspected trigger foods, drugs, or environmental agents."
        ],
        "medications_otc": "Second-generation non-sedating oral antihistamines (Cetirizine, Fexofenadine, Levocetirizine).",
        "when_to_see_doctor": "EMERGENCY if throat tightens, tongue swells, or breathing becomes laboured."
    },
    "fungal_infection": {
        "name": "Fungal Skin Infection (Tinea / Ringworm)",
        "category": "Dermatological Diseases",
        "severity": "mild",
        "primary_symptoms": ["circular_ring_shaped_red_rash", "itching", "raised_scaly_borders", "clear_skin_in_center"],
        "secondary_symptoms": ["dry_peeling_skin", "burning", "discolored_patches"],
        "red_flags": ["Spreading rapidly to face, groin, or scalp", "Painful secondary bacterial cellulitis"],
        "description": "A common superficial fungal infection of keratinized skin tissues caused by dermatophytes.",
        "home_care": [
            "Keep the affected skin clean and completely dry.",
            "Change clothes and undergarments daily; wash in hot water.",
            "Do not share towels, combs, or personal items.",
            "Avoid tight-fitting, non-breathable footwear and synthetic fabrics."
        ],
        "medications_otc": "Topical antifungal creams (Clotrimazole, Terbinafine, Miconazole) applied twice daily for 2-4 weeks.",
        "when_to_see_doctor": "If rash fails to improve after 2 weeks of consistent OTC antifungal application."
    },

    # ==================== MUSCULOSKELETAL DISEASES ====================
    "osteoarthritis": {
        "name": "Osteoarthritis (Degenerative Joint Disease)",
        "category": "Musculoskeletal Diseases",
        "severity": "moderate",
        "primary_symptoms": ["joint_pain_worse_with_activity", "joint_stiffness_in_morning_under_30min", "crepitus_grating_sound", "reduced_range_of_motion"],
        "secondary_symptoms": ["joint_swelling", "bony_enlargements_nodes", "muscle_weakness_around_joint"],
        "red_flags": ["Hot, intensely red, acutely swollen joint with fever (Septic arthritis emergency)", "Inability to bear any weight"],
        "description": "Wear-and-tear degradation of articular cartilage cushioning the ends of bones, commonly affecting knees, hips, hands, and spine.",
        "home_care": [
            "Low-impact exercises: swimming, stationary cycling, walking.",
            "Weight management to relieve compressive joint loads.",
            "Apply moist heat for stiffness; cold packs for post-exercise swelling.",
            "Use supportive footwear or knee braces."
        ],
        "medications_otc": "Topical NSAID gel (Diclofenac gel), Paracetamol for mild discomfort.",
        "when_to_see_doctor": "Orthopedic or rheumatologic evaluation with X-rays."
    },
    "rheumatoid_arthritis": {
        "name": "Rheumatoid Arthritis (Autoimmune)",
        "category": "Musculoskeletal Diseases",
        "severity": "high",
        "primary_symptoms": ["symmetrical_joint_swelling_both_hands_wrists", "prolonged_morning_stiffness_over_1hr", "joint_warmth_redness", "fatigue"],
        "secondary_symptoms": ["low_grade_fever", "loss_of_appetite", "rheumatoid_nodules_under_skin", "weakness"],
        "red_flags": ["Severe cervical spine pain with arm numbness", "Eye pain and redness (scleritis)"],
        "description": "A chronic systemic autoimmune disorder causing persistent inflammation of the synovial membrane, potentially leading to bone erosion and joint deformity.",
        "home_care": [
            "Balance gentle mobility exercises with rest during flare-ups.",
            "Eat an anti-inflammatory Mediterranean diet (rich in omega-3 fatty acids, olive oil, berries).",
            "Protect joints with assistive devices and ergonomic handles."
        ],
        "medications_otc": "Requires early Disease-Modifying Anti-Rheumatic Drugs (DMARDs, e.g. Methotrexate) prescribed by a rheumatologist.",
        "when_to_see_doctor": "Urgent rheumatology consultation. Early treatment prevents irreversible joint deformity."
    },
    "lumbar_strain": {
        "name": "Acute Lumbar Muscle Strain / Back Spasm",
        "category": "Musculoskeletal Diseases",
        "severity": "mild",
        "primary_symptoms": ["lower_back_pain_stiffness", "muscle_spasms_in_lower_back", "pain_worse_with_bending_lifting"],
        "secondary_symptoms": ["difficulty_standing_straight", "tenderness_in_lumbar_muscles", "limited_mobility"],
        "red_flags": ["Loss of bowel or bladder control (Cauda Equina emergency)", "Numbness in groin/saddle area", "Weakness causing foot drop"],
        "description": "Stretching or tearing of muscle fibers or tendons in the lower back, usually following improper lifting or sudden twisting movements.",
        "home_care": [
            "Avoid prolonged bed rest; engage in light walking to prevent spinal stiffness.",
            "Apply ice pack for first 48 hours (15 min at a time), then switch to moist heat.",
            "Sleep on your side with a pillow between knees or on your back with a pillow under knees.",
            "Perform gentle pelvic tilts and hamstring stretches as pain allows."
        ],
        "medications_otc": "Ibuprofen or Paracetamol, topical pain relief gels/patches.",
        "when_to_see_doctor": "If back pain radiates down past the knee, causes numbness, or bowel/bladder dysfunction occurs."
    },

    # ==================== URINARY & RENAL DISEASES ====================
    "uti": {
        "name": "Urinary Tract Infection (UTI / Cystitis)",
        "category": "Urinary & Renal Diseases",
        "severity": "moderate",
        "primary_symptoms": ["burning_pain_with_urination_dysuria", "frequent_urgent_need_to_urinate", "cloudy_foul_smelling_urine", "lower_pelvic_pain"],
        "secondary_symptoms": ["low_fever", "microscopic_blood_in_urine", "fatigue"],
        "red_flags": ["High fever with shaking chills", "Flank or mid-back pain over kidneys", "Nausea and vomiting (Pyelonephritis / Kidney infection)"],
        "description": "A bacterial infection of the urinary tract, most commonly affecting the bladder and urethra.",
        "home_care": [
            "Drink plenty of water (2.5 - 3 liters daily) to flush bacteria from the urinary tract.",
            "Urinate whenever the urge arises; do not hold urine.",
            "Apply a warm heating pad to lower abdomen to soothe cramps.",
            "Avoid caffeine, alcohol, and carbonated beverages which irritate the bladder."
        ],
        "medications_otc": "Phenazopyridine for temporary urinary burning relief (colors urine bright orange). Requires prescription antibiotics.",
        "when_to_see_doctor": "Urine routine/culture test and targeted antibiotic course required."
    },
    "kidney_stones": {
        "name": "Renal Calculi (Kidney Stones / Nephrolithiasis)",
        "category": "Urinary & Renal Diseases",
        "severity": "high",
        "primary_symptoms": ["severe_sharp_flank_back_pain", "pain_radiating_to_lower_abdomen_groin", "pain_comes_in_waves", "blood_in_urine_pink_red"],
        "secondary_symptoms": ["nausea_and_vomiting", "painful_urination", "frequent_urination", "fever_if_infected"],
        "red_flags": ["Fever and chills accompanying severe flank pain (infected obstructed stone)", "Inability to urinate at all", "Intractable pain"],
        "description": "Hard mineral deposits (calcium oxalate, uric acid) that form in the kidneys and cause excruciating colicky pain as they pass through the ureter.",
        "home_care": [
            "Drink 2-3 liters of water daily to assist stone passage (if instructed by physician).",
            "Filter urine through a fine mesh to catch any passed stone for laboratory mineral analysis.",
            "Apply warm compress to the aching flank area."
        ],
        "medications_otc": "NSAIDs (Ibuprofen, Ketorolac) under medical supervision. Prescription alpha-blockers (Tamsulosin) may be prescribed.",
        "when_to_see_doctor": "Urgent ultrasound/CT KUB scan required."
    }
}


# Categorized symptom definitions with standardized tokens and display names
SYMPTOM_CATEGORIES = {
    "General & Systemic": [
        ("fever", "Fever"),
        ("high_fever", "High Fever (>102°F)"),
        ("low_fever", "Low-grade Fever"),
        ("chills", "Chills & Shivering"),
        ("sweating", "Profuse Sweating"),
        ("night_sweats", "Night Sweats"),
        ("fatigue", "Extreme Fatigue / Weakness"),
        ("unexplained_weight_loss", "Unexplained Weight Loss"),
        ("unexplained_weight_gain", "Unexplained Weight Gain"),
        ("loss_of_appetite", "Loss of Appetite"),
        ("excessive_thirst", "Excessive Thirst")
    ],
    "Head, Eyes, Ears & Throat": [
        ("headache", "Headache"),
        ("severe_headache", "Severe Throbbing Headache"),
        ("throbbing_one_sided_headache", "One-sided Head Pain (Migraine)"),
        ("pain_behind_eyes", "Pain Behind Eyes"),
        ("dizziness", "Dizziness / Lightheadedness"),
        ("spinning_sensation", "Spinning Sensation (Vertigo)"),
        ("sore_throat", "Sore Throat / Throat Pain"),
        ("runny_nose", "Runny / Stuffy Nose"),
        ("sneezing", "Frequent Sneezing"),
        ("nasal_congestion", "Nasal Congestion / Blockage"),
        ("loss_of_taste_smell", "Loss of Taste or Smell"),
        ("facial_pain_pressure", "Facial Pain / Sinus Pressure"),
        ("sensitivity_to_light_photophobia", "Sensitivity to Light"),
        ("sensitivity_to_sound_phonophobia", "Sensitivity to Sound"),
        ("yellow_eyes_skin", "Yellowish Eyes or Skin (Jaundice)"),
        ("blurry_vision", "Blurry Vision")
    ],
    "Chest & Respiratory": [
        ("dry_cough", "Dry Cough"),
        ("persistent_cough_with_mucus", "Cough with Mucus / Phlegm"),
        ("chronic_cough", "Chronic Persistent Cough"),
        ("coughing_blood", "Coughing up Blood"),
        ("shortness_of_breath", "Shortness of Breath / Breathlessness"),
        ("wheezing", "Wheezing / Whistling Breath"),
        ("chest_tightness", "Chest Tightness"),
        ("chest_pressure_squeezing", "Chest Pressure / Squeezing Pain"),
        ("pain_radiating_to_arm_neck_jaw", "Pain Radiating to Left Arm / Jaw"),
        ("palpitations_racing_heart", "Heart Palpitations / Rapid Heartbeat"),
        ("cold_sweating", "Cold Sweats")
    ],
    "Stomach & Digestive": [
        ("nausea", "Nausea"),
        ("vomiting", "Vomiting"),
        ("watery_diarrhea", "Watery Diarrhea"),
        ("abdominal_cramps", "Abdominal Cramps"),
        ("stomach_pain", "Stomach Ache"),
        ("sudden_pain_lower_right_abdomen", "Severe Lower Right Abdomen Pain"),
        ("heartburn_burning_chest", "Heartburn / Acid Reflux"),
        ("burning_stomach_pain_between_meals", "Burning Stomach Pain"),
        ("bloating", "Abdominal Bloating & Gas"),
        ("dark_urine", "Dark / Tea-colored Urine"),
        ("pale_stools", "Pale / Clay-colored Stools")
    ],
    "Musculoskeletal & Joints": [
        ("joint_pain", "Joint Pain"),
        ("joint_stiffness_in_morning_under_30min", "Morning Joint Stiffness"),
        ("symmetrical_joint_swelling_both_hands_wrists", "Swollen Joints in Both Hands"),
        ("muscle_pain", "Muscle Aches / Body Pain"),
        ("severe_body_ache", "Severe Body Ache"),
        ("lower_back_pain_stiffness", "Lower Back Pain & Stiffness")
    ],
    "Skin & Allergies": [
        ("skin_rash", "Skin Rash / Spots"),
        ("intense_skin_itching", "Intense Skin Itching"),
        ("raised_red_itchy_welts_wheals", "Raised Hives / Welts"),
        ("dry_cracked_scaly_skin", "Dry, Scaly Skin"),
        ("circular_ring_shaped_red_rash", "Circular Ring-shaped Rash")
    ],
    "Urinary & Renal": [
        ("burning_pain_with_urination_dysuria", "Burning Pain While Urinating"),
        ("frequent_urination", "Frequent Urination"),
        ("blood_in_urine_pink_red", "Blood in Urine"),
        ("severe_sharp_flank_back_pain", "Severe Flank / Kidney Pain")
    ]
}


# Natural language keywords and aliases mapped to standardized symptom tokens
SYMPTOM_SYNONYMS = {
    # Fever & Systemic
    "fever": "fever", "high fever": "high_fever", "temperature": "fever", "pyrexia": "fever",
    "fevers": "fever", "feverish": "fever", "high temperature": "high_fever", "running temperature": "high_fever",
    "fever 100": "high_fever", "fever 101": "high_fever", "fever 102": "high_fever", "fever 103": "high_fever",
    "100 fever": "high_fever", "101 fever": "high_fever", "102 fever": "high_fever", "103 fever": "high_fever",
    "chills": "chills", "shivering": "chills", "shiver": "chills", "shivers": "chills",
    "sweating": "sweating", "sweats": "sweating", "night sweats": "night_sweats",

    # Head & Neurological
    "headache": "headache", "headaches": "headache", "head pain": "headache", "head ache": "headache",
    "head hurts": "headache", "head hurting": "headache", "heavy head": "headache", "head heaviness": "headache",
    "migraine": "throbbing_one_sided_headache", "migraines": "throbbing_one_sided_headache",
    "throbbing head": "throbbing_one_sided_headache", "one sided headache": "throbbing_one_sided_headache",
    "photophobia": "sensitivity_to_light_photophobia", "light sensitivity": "sensitivity_to_light_photophobia",
    "dizziness": "dizziness", "dizzy": "dizziness", "giddiness": "dizziness", "giddy": "dizziness",
    "lightheaded": "dizziness", "lightheadedness": "dizziness", "vertigo": "spinning_sensation",
    "spinning": "spinning_sensation",

    # Eyes & ENT
    "sore throat": "sore_throat", "throat pain": "sore_throat", "throat irritation": "sore_throat",
    "throat hurts": "sore_throat", "throat hurting": "sore_throat", "throat infection": "sore_throat",
    "itchy throat": "sore_throat", "throat itching": "sore_throat",
    "runny nose": "runny_nose", "running nose": "runny_nose", "cold": "runny_nose", "colds": "runny_nose",
    "sneezing": "sneezing", "congestion": "nasal_congestion", "blocked nose": "nasal_congestion",
    "stuffy nose": "nasal_congestion", "sinus": "facial_pain_pressure", "sinus pain": "facial_pain_pressure",
    "facial pain": "facial_pain_pressure", "yellow eyes": "yellow_eyes_skin", "jaundice": "yellow_eyes_skin",
    "yellow skin": "yellow_eyes_skin", "loss of smell": "loss_of_taste_smell", "loss of taste": "loss_of_taste_smell",
    "taste lost": "loss_of_taste_smell", "eye pain": "pain_behind_eyes", "pain behind eyes": "pain_behind_eyes",

    # Respiratory & Cardiac
    "cough": "dry_cough", "coughs": "dry_cough", "coughing": "dry_cough", "coughed": "dry_cough",
    "dry cough": "dry_cough", "wet cough": "persistent_cough_with_mucus",
    "cough with phlegm": "persistent_cough_with_mucus", "cough with mucus": "persistent_cough_with_mucus",
    "phlegm": "persistent_cough_with_mucus", "mucus": "persistent_cough_with_mucus",
    "coughing blood": "coughing_blood", "blood in cough": "coughing_blood", "hemoptysis": "coughing_blood",
    "shortness of breath": "shortness_of_breath", "breathless": "shortness_of_breath", "breathlessness": "shortness_of_breath",
    "breathing problem": "shortness_of_breath", "difficulty breathing": "shortness_of_breath", "trouble breathing": "shortness_of_breath",
    "wheezing": "wheezing", "wheeze": "wheezing", "chest tight": "chest_tightness", "chest tightness": "chest_tightness",
    "chest pain": "chest_pressure_squeezing", "chest pressure": "chest_pressure_squeezing", "chest hurts": "chest_pressure_squeezing",
    "chest heaviness": "chest_pressure_squeezing", "heart pain": "chest_pressure_squeezing",
    "pain radiating to arm": "pain_radiating_to_arm_neck_jaw", "left arm pain": "pain_radiating_to_arm_neck_jaw",
    "jaw pain": "pain_radiating_to_arm_neck_jaw", "palpitations": "palpitations_racing_heart",
    "palpitation": "palpitations_racing_heart", "racing heart": "palpitations_racing_heart",
    "fast heartbeat": "palpitations_racing_heart", "rapid heartbeat": "palpitations_racing_heart",
    "heart racing": "palpitations_racing_heart", "fluttering heart": "palpitations_racing_heart",
    "cold sweat": "cold_sweating", "cold sweating": "cold_sweating",

    # Gastrointestinal & Abdominal
    "nausea": "nausea", "nauseous": "nausea", "nauseated": "nausea", "vomit": "vomiting", "vomits": "vomiting",
    "vomited": "vomiting", "vomiting": "vomiting", "throw up": "vomiting", "throwing up": "vomiting",
    "vomit sensation": "nausea", "vomiting sensation": "nausea", "feeling like vomiting": "nausea",
    "diarrhea": "watery_diarrhea", "diarrhoea": "watery_diarrhea", "loose motions": "watery_diarrhea",
    "loose motion": "watery_diarrhea", "motions": "watery_diarrhea", "motions problem": "watery_diarrhea",
    "loose stools": "watery_diarrhea", "loose stool": "watery_diarrhea", "watery stool": "watery_diarrhea",
    "watery stools": "watery_diarrhea", "frequent motions": "watery_diarrhea",
    "food poisoning": "watery_diarrhea", "upset stomach": "watery_diarrhea", "stomach upset": "watery_diarrhea",
    "stomach pain": "stomach_pain", "stomach ache": "stomach_pain", "stomachache": "stomach_pain",
    "stomach hurts": "stomach_pain", "stomach hurting": "stomach_pain", "stomach paining": "stomach_pain",
    "tummy pain": "stomach_pain", "tummy ache": "stomach_pain", "tummy hurts": "stomach_pain",
    "belly pain": "stomach_pain", "belly ache": "stomach_pain", "abdominal pain": "stomach_pain",
    "stomach cramp": "abdominal_cramps", "stomach cramps": "abdominal_cramps", "abdominal cramps": "abdominal_cramps",
    "right lower stomach pain": "sudden_pain_lower_right_abdomen", "appendicitis pain": "sudden_pain_lower_right_abdomen",
    "heartburn": "heartburn_burning_chest", "acidity": "heartburn_burning_chest", "acid reflux": "heartburn_burning_chest",
    "gerd": "heartburn_burning_chest", "gastric": "heartburn_burning_chest", "gastric trouble": "heartburn_burning_chest",
    "gastric problem": "heartburn_burning_chest", "gastric pain": "heartburn_burning_chest",
    "gas": "bloating", "gas trouble": "bloating", "bloating": "bloating", "indigestion": "bloating",
    "burning stomach": "burning_stomach_pain_between_meals", "dark urine": "dark_urine", "pale stool": "pale_stools",
    "loss of appetite": "loss_of_appetite", "no appetite": "loss_of_appetite",

    # Endocrine & Systemic
    "fatigue": "fatigue", "tired": "fatigue", "tiredness": "fatigue", "weakness": "fatigue", "weak": "fatigue",
    "exhaustion": "fatigue", "exhausted": "fatigue", "drowsy": "fatigue", "loss of energy": "fatigue",
    "unwell": "fatigue", "feeling unwell": "fatigue", "not feeling well": "fatigue", "not well": "fatigue",
    "feeling sick": "fatigue", "sick": "fatigue",
    "weight loss": "unexplained_weight_loss", "weight gain": "unexplained_weight_gain",
    "thirst": "excessive_thirst", "frequent thirst": "excessive_thirst", "drinking lot of water": "excessive_thirst",
    "frequent urination": "frequent_urination", "urinating often": "frequent_urination", "pee often": "frequent_urination",
    "burning urination": "burning_pain_with_urination_dysuria", "pain peeing": "burning_pain_with_urination_dysuria",
    "dysuria": "burning_pain_with_urination_dysuria", "flank pain": "severe_sharp_flank_back_pain",
    "kidney pain": "severe_sharp_flank_back_pain", "blood in urine": "blood_in_urine_pink_red",

    # Musculoskeletal & Skin
    "joint pain": "joint_pain", "joint ache": "joint_pain", "joint aches": "joint_pain",
    "knee pain": "joint_pain", "knees pain": "joint_pain", "stiff joints": "joint_stiffness_in_morning_under_30min",
    "body pain": "muscle_pain", "body paining": "muscle_pain", "body ache": "severe_body_ache",
    "body aches": "severe_body_ache", "body hurts": "severe_body_ache", "body hurting": "severe_body_ache",
    "muscle ache": "muscle_pain", "muscle pain": "muscle_pain", "muscle cramps": "muscle_pain", "sprain": "muscle_pain",
    "back pain": "lower_back_pain_stiffness", "back ache": "lower_back_pain_stiffness", "backache": "lower_back_pain_stiffness",
    "back hurts": "lower_back_pain_stiffness", "lower back pain": "lower_back_pain_stiffness",
    "leg pain": "joint_pain", "legs pain": "joint_pain", "legs aching": "joint_pain",
    "rash": "skin_rash", "skin rash": "skin_rash", "spots": "skin_rash", "itching": "intense_skin_itching",
    "itchy": "intense_skin_itching", "hives": "raised_red_itchy_welts_wheals", "welts": "raised_red_itchy_welts_wheals",
    "ringworm": "circular_ring_shaped_red_rash", "scaly skin": "dry_cracked_scaly_skin",

    # ==================== KANNADA LANGUAGE SYNONYMS ====================
    # Fever & Chills (ಜ್ವರ / ಚಳಿ)
    "ಜ್ವರ": "fever", "ತೀವ್ರ ಜ್ವರ": "high_fever", "ಅತಿಯಾದ ಜ್ವರ": "high_fever",
    "ಸಾಧಾರಣ ಜ್ವರ": "mild_fever", "ಚಳಿ": "chills", "ನಡುಕ": "chills",
    "ಬೆವರು": "sweating", "ರಾತ್ರಿ ಬೆವರು": "night_sweats", "ಬಿಸಿ ಮೈ": "fever",
    "ಜ್ವರ ಬಂದಿದೆ": "fever", "ಜ್ವರವಿದೆ": "fever", "ಜ್ವರವಾಗಿದೆ": "fever",
    "jwara": "fever", "jvara": "fever", "jwara ide": "fever", "jvara ide": "fever",
    "nanage jwara": "fever", "nanage jvara": "fever", "jwara bandide": "fever",
    "tivra jwara": "high_fever", "chali": "chills", "naduka": "chills",

    # Head & Neurological (ತಲೆ / ನರಗಳು)
    "ತಲೆನೋವು": "headache", "ತೀವ್ರ ತಲೆನೋವು": "severe_headache", "ಮೈಗ್ರೇನ್": "throbbing_one_sided_headache",
    "ತಲೆಸುತ್ತು": "dizziness", "ತಲೆ ತಿರುಗುವುದು": "dizziness", "ತಲೆ ಗಿರ್ರೆನ್ನುವುದು": "spinning_sensation",
    "ತಲೆ ಭಾರ": "headache", "ತಲೆಭಾರ": "headache", "ಬೆಳಕಿನ ಸೂಕ್ಷ್ಮತೆ": "sensitivity_to_light_photophobia",
    "talenovu": "headache", "tale novu": "headache", "talenovu ide": "headache", "tale novu ide": "headache",
    "thale novu": "headache", "thalenovu": "headache", "talesuttu": "dizziness", "tale suttu": "dizziness",

    # Eyes & ENT (ಕಣ್ಣು / ಕಿವಿ / ಮೂಗು / ಗಂಟಲು)
    "ಗಂಟಲು ನೋವು": "sore_throat", "ಗಂಟಲು ಕೆರೆತ": "sore_throat", "ಗಂಟಲು ಉರಿ": "sore_throat",
    "ನೆಗಡಿ": "runny_nose", "ನೆಗಡಿ ಆಗಿದೆ": "runny_nose", "ಶೀತ": "runny_nose", "ಮೂಗು ಕಟ್ಟುವುದು": "nasal_congestion",
    "ಸೀನು": "sneezing", "ಕಣ್ಣು ನೋವು": "pain_behind_eyes", "ಕಣ್ಣಿನ ಹಿಂಭಾಗದ ನೋವು": "pain_behind_eyes",
    "ಹಳದಿ ಕಣ್ಣುಗಳು": "yellow_eyes_skin", "ಹಳದಿ ಚರ್ಮ": "yellow_eyes_skin", "ಕಾಮಾಲೆ": "yellow_eyes_skin",
    "ರುಚಿ ನಷ್ಟ": "loss_of_taste_smell", "ವಾಸನೆ ನಷ್ಟ": "loss_of_taste_smell",
    "gantalu novu": "sore_throat", "gantlu novu": "sore_throat", "negadi": "runny_nose",
    "sheetha": "runny_nose", "sheeta": "runny_nose", "kamale": "yellow_eyes_skin",

    # Respiratory & Cardiac (ಉಸಿರಾಟ / ಎದೆ)
    "ಕೆಮ್ಮು": "dry_cough", "ಒಣ ಕೆಮ್ಮು": "dry_cough", "ನೆಗಡಿ ಕೆಮ್ಮು": "dry_cough",
    "ಕೆಮ್ಮು ಬರ್ತಿದೆ": "dry_cough", "ಕೆಮ್ಮು ಬರುತ್ತಿದೆ": "dry_cough", "ಕೆಮ್ಮಿದೆ": "dry_cough",
    "ಕಫ": "persistent_cough_with_mucus", "ಲೋಳೆ": "persistent_cough_with_mucus",
    "ರಕ್ತ ಕೆಮ್ಮು": "coughing_blood", "ಉಸಿರಾಟದ ತೊಂದರೆ": "shortness_of_breath",
    "ಉಸಿರಾಟ ಕಷ್ಟ": "shortness_of_breath", "ಉಸಿರಾಡಲು ಕಷ್ಟ": "shortness_of_breath",
    "ಉಸಿರು ಕಟ್ಟುವಿಕೆ": "shortness_of_breath", "ದಮ್ಮು": "shortness_of_breath", "ಉಬ್ಬಸ": "wheezing",
    "ಎದೆ ನೋವು": "chest_pressure_squeezing", "ಎದೆ ಬಿಗಿತ": "chest_tightness",
    "ಎದೆ ಬಡಿತ": "palpitations_racing_heart", "ಗುಂಡಿಗೆ ಬಡಿತ": "palpitations_racing_heart",
    "ತಣ್ಣನೆಯ ಬೆವರು": "cold_sweating", "ಎದೆಯಲ್ಲಿ ನೋವು": "chest_pressure_squeezing",
    "kemmu": "dry_cough", "kemmu ide": "dry_cough", "kemmu bartide": "dry_cough",
    "ede novu": "chest_pressure_squeezing", "edenovu": "chest_pressure_squeezing",
    "ede novu ide": "chest_pressure_squeezing", "usirata samasye": "shortness_of_breath",

    # Gastrointestinal (ಹೊಟ್ಟೆ / ಜೀರ್ಣಾಂಗ)
    "ವಾಂತಿ": "vomiting", "ವಾಕರಿಕೆ": "nausea", "ಹೊಟ್ಟೆ ನೋವು": "stomach_pain",
    "ಹೊಟ್ಟೆ ನೋಯ್ತಿದೆ": "stomach_pain", "ಹೊಟ್ಟೆಯಲ್ಲಿ ನೋವು": "stomach_pain", "ಹೊಟ್ಟೆ ಕೆಟ್ಟಿದೆ": "stomach_pain",
    "ಹೊಟ್ಟೆ ಸೆಳೆತ": "abdominal_cramps", "ಹೊಟ್ಟೆ ಉಬ್ಬರ": "bloating", "ಅಜೀರ್ಣ": "bloating",
    "ಬೇದಿ": "watery_diarrhea", "ಅತಿಸಾರ": "watery_diarrhea", "ನೀರು ಬೇದಿ": "watery_diarrhea",
    "ಆಹಾರ ವಿಷಾಹಾರ": "watery_diarrhea", "ವಿಷಾಹಾರ": "watery_diarrhea",
    "ಎದೆಯುರಿ": "heartburn_burning_chest", "ಅಸಿಡಿಟಿ": "heartburn_burning_chest",
    "ಹಸಿವಿಲ್ಲದಿರುವುದು": "loss_of_appetite", "ಹಸಿವಿಲ್ಲ": "loss_of_appetite", "ಹಸಿವಾಗದಿರುವುದು": "loss_of_appetite",
    "vaanthi": "vomiting", "vaanti": "vomiting", "vanti": "vomiting", "vakarike": "nausea",
    "hotte novu": "stomach_pain", "hottenovu": "stomach_pain", "hotte novu ide": "stomach_pain",
    "bedi": "watery_diarrhea", "bhedi": "watery_diarrhea", "neeru bedi": "watery_diarrhea",

    # Endocrine, Musculoskeletal, General Wellness & Skin (ದೇಹ / ಚರ್ಮ / ಮೂತ್ರ)
    "ಸುಸ್ತು": "fatigue", "ಆಯಾಸ": "fatigue", "ದಣಿವು": "fatigue", "ನಿಶ್ಯಕ್ತಿ": "fatigue",
    "ಹುಷಾರಿಲ್ಲ": "fatigue", "ನನಗೆ ಹುಷಾರಿಲ್ಲ": "fatigue", "ಆರಾಮ ಇಲ್ಲ": "fatigue", "ನನಗೆ ಆರಾಮ ಇಲ್ಲ": "fatigue",
    "ಮೈಕೈ ನೋವು": "muscle_pain", "ಮೈ ಕೈ ನೋವು": "muscle_pain", "ಮೈಕೈನೋವು": "muscle_pain",
    "ಮೈ ನೋವು": "severe_body_ache", "ಕೀಲು ನೋವು": "joint_pain", "ಮಂಡಿ ನೋವು": "joint_pain",
    "ಬೆನ್ನು ನೋವು": "lower_back_pain_stiffness", "ಬೆನ್ನಿನಲ್ಲಿ ನೋವು": "lower_back_pain_stiffness",
    "ಕಾಲು ನೋವು": "joint_pain", "ಕಾಲಿನಲ್ಲಿ ನೋವು": "joint_pain", "ಕೈ ನೋವು": "muscle_pain", "ಕೈಯಲ್ಲಿ ನೋವು": "muscle_pain",
    "ತುರಿಕೆ": "intense_skin_itching", "ದದ್ದು": "skin_rash", "ಚರ್ಮದ ದದ್ದು": "skin_rash",
    "ಮೂತ್ರದಲ್ಲಿ ಉರಿ": "burning_pain_with_urination_dysuria", "ಹೆಚ್ಚು ಮೂತ್ರ": "frequent_urination",
    "ಹೆಚ್ಚು ಬಾಯಾರಿಕೆ": "excessive_thirst", "ಬಾಯಾರಿಕೆ": "excessive_thirst", "ತೂಕ ನಷ್ಟ": "unexplained_weight_loss",
    "susthu": "fatigue", "sustu": "fatigue", "susthu ide": "fatigue", "sustu ide": "fatigue",
    "ayasa": "fatigue", "maikai novu": "muscle_pain", "mai kai novu": "muscle_pain",
    "keelu novu": "joint_pain", "mandi novu": "joint_pain", "mandinovu": "joint_pain",
    "kaalu novu": "joint_pain", "kalu novu": "joint_pain", "kai novu": "muscle_pain",
    "bennu novu": "lower_back_pain_stiffness", "bennunovu": "lower_back_pain_stiffness",
    "hushaarilla": "fatigue", "husharilla": "fatigue", "nanage husharilla": "fatigue",
    "arama illa": "fatigue", "aarama illa": "fatigue",

    # ==================== HINDI / HINGLISH LANGUAGE SYNONYMS ====================
    "बुखार": "fever", "तेज बुखार": "high_fever", "सिरदर्द": "headache", "सिर दर्द": "headache",
    "खांसी": "dry_cough", "जुकाम": "runny_nose", "सर्दी": "runny_nose", "उल्टी": "vomiting",
    "दस्त": "watery_diarrhea", "पेट दर्द": "stomach_pain", "सीने में दर्द": "chest_pressure_squeezing",
    "कमजोरी": "fatigue", "थकान": "fatigue", "चक्कर": "dizziness", "गले में खराश": "sore_throat",
    "बदन दर्द": "severe_body_ache", "तबीयत खराब": "fatigue", "बीमार": "fatigue",
    "tabiyat kharab": "fatigue", "bimar": "fatigue", "sirdard": "headache", "pet dard": "stomach_pain",
    "dast": "watery_diarrhea", "ulti": "vomiting", "chakkar": "dizziness", "kamzori": "fatigue",
    "badan dard": "severe_body_ache", "gale me dard": "sore_throat"
}
