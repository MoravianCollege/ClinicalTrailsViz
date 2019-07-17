from AWS_AACT_Pipeline.src.AWS_AACT_Pipeline.condition_type import ConditionCategorizer


categorizer = ConditionCategorizer("../conditions_key")
categorizer.read_file_conditions()


def get_result(name):
    return categorizer.check_conditions(name)


def test_empty_entry_is_other():
    assert get_result("") == "Other"
    assert get_result(" ") == "Other"
    assert get_result("pain") == "Other"


def test_oncology():
    assert get_result("kidney cancer") == "Oncology"
    assert get_result("aggressive non-hodgkin lymphoma") == "Oncology"
    assert get_result("blahcancerblah") == "Oncology"


def test_neurology():
    assert get_result("brain") == "Neurology"
    assert get_result("traumatic brain injury") == "Neurology"
    assert get_result("brain cancer") != "Neurology"


def test_metobolic_and_endocrine():
    assert get_result("diabetes") == "Metabolic & Endocrine"
    assert get_result("impaired insulin secretion") == "Metabolic & Endocrine"
    assert get_result("malnutrition") == "Metabolic & Endocrine"


def test_cardiovascular():
    assert get_result("cardiovas") == "Cardiovascular"
    assert get_result("heart disease") == "Cardiovascular"
    assert get_result("coronary artery disease") == "Cardiovascular"


def test_infection():
    assert get_result("influenza") == "Infection"
    assert get_result(" infection ") == "Infection"
    assert get_result("hepatitis c") == "Infection"


def test_respiratory():
    assert get_result("smoking") == "Respiratory"
    assert get_result("respiratory distress syndrome") == "Respiratory"
    assert get_result("asthma") == "Respiratory"


def test_renal_and_urogenital():
    assert get_result("kidney transplant") == "Renal & Urogenital"
    assert get_result("renal insufficiency") == "Renal & Urogenital"
    assert get_result("cardiorenal") != "Renal & Urogenital"


def test_mental_health():
    assert get_result("schizoaffective disorder	") == "Mental Health"
    assert get_result("major depressive disorder") == "Mental Health"
    assert get_result("bipolar disorder") == "Mental Health"


def test_congenital():
    assert get_result("cystic fibrosis in children") == "Congenital Disorders"
    assert get_result("cerebral palsy") == "Congenital Disorders"


def test_musculoskeletal():
    assert get_result("knee osteoarthritis") == "Musculoskeletal"
    assert get_result("fibromyalgia") == "Musculoskeletal"


def test_immune_and_inflammatory():
    assert get_result("rheumatoid arthritis") == "Inflammatory & Immune"
    assert get_result("pelvic inflammatory disease") == "Inflammatory & Immune"


def test_oral_and_gastrointestinal():
    assert get_result("crohn's disease") == "Oral & Gastrointestinal"
    assert get_result("irritable bowel syndrome") == "Oral & Gastrointestinal"


def test_reproductive():
    assert get_result("art") == "Reproductive"
    assert get_result("artery") != "Reproductive"
    assert get_result("cart") != "Reproductive"
    assert get_result("teen pregnancy prevention") == "Reproductive"


def test_blood():
    assert get_result("aplastic anemia") == "Blood"
    assert get_result("myelodysplastic syndrome") == "Blood"


def test_skin():
    assert get_result("dermatology") == "Skin"
    assert get_result("psoriasis") == "Skin"
    assert get_result("atopic dermatitis") == "Skin"

def test_eye():
    assert get_result("cataract") == "Eye"
    assert get_result("high myopia") == "Eye"
    assert get_result("glaucoma") == "Eye"

def test_stroke():
    assert get_result("ischemic stroke") == "Stroke"
    assert get_result(" stroke ") == "Stroke"

def test_healthy():
    assert get_result("healthy volunteers") == "Healthy"


if __name__ == "__main__":
    test_empty_entry_is_other()
    test_oncology()
    test_neurology()
    test_metobolic_and_endocrine()
    test_cardiovascular()
    test_infection()
    test_respiratory()
    test_renal_and_urogenital()
    test_mental_health()
    test_congenital()
    test_musculoskeletal()
    test_immune_and_inflammatory()
    test_oral_and_gastrointestinal()
    test_reproductive()
    test_blood()
    test_skin()
    test_eye()
    test_stroke()
    test_healthy()
    print("Everything passed")
