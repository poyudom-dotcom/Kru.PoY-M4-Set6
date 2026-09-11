import sys
import os
import subprocess

# ==============================================================================
# ⚙️ ชุดทดสอบข้อสอบทั้ง 5 ข้อสำหรับ Kru.PoY-M4-Set6 (ข้อละ 4 เคส = ข้อละ 4 คะแนน)
# ==============================================================================
EXAM_TEST_CASES = {
    # ข้อ 1: คำนวณคะแนนเฉลี่ย 3 วิชา ((s1 + s2 + s3) / 3)
    "Examination_1.py": [
        (["10", "20", "30"], "20.0"),
        (["15", "15", "15"], "15.0"),
        (["80", "90", "100"], "90.0"),
        (["0", "0", "0"], "0.0")
    ],
    # ข้อ 2: ตรวจสอบความสูงสำหรับเล่นเครื่องเล่น (>=140 Can Ride, <140 Cannot Ride)
    "Examination_2.py": [
        (["150"], "Can Ride"),
        (["140"], "Can Ride"),
        (["139"], "Cannot Ride"),
        (["120"], "Cannot Ride")
    ],
    # ข้อ 3: ตรวจสอบการหาร 5 ลงตัว (Yes / No)
    "Examination_3.py": [
        (["25"], "Yes"),
        (["0"], "Yes"),
        (["12"], "No"),
        (["-5"], "Yes")
    ],
    # ข้อ 4: คำนวณค่าจัดส่งสินค้าตามน้ำหนัก (<=1kg: 30, <=5kg: 50, >5kg: 100)
    "Examination_4.py": [
        (["0.5"], "30"),
        (["1"], "30"),
        (["3.5"], "50"),
        (["6"], "100")
    ],
    # ข้อ 5: บอกช่วงเวลาจากนาฬิกา 24 ชั่วโมง (<12: Morning, 12-17: Afternoon, >=18: Night)
    "Examination_5.py": [
        (["8"], "Morning"),
        (["12"], "Afternoon"),
        (["15"], "Afternoon"),
        (["20"], "Night")
    ]
}

def find_file(base_name):
    """ค้นหาไฟล์รองรับทั้งชื่อที่มีและไม่มี .py"""
    if os.path.exists(base_name):
        return base_name
    elif os.path.exists(f"{base_name}.py"):
        return f"{base_name}.py"
    elif os.path.exists(base_name.replace(".py", "")):
        return base_name.replace(".py", "")
    return None

def run_test(file_path, inputs):
    """รันไฟล์และดึงค่า Output"""
    try:
        input_data = "\n".join(inputs)
        process = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3,
            encoding='utf-8',
            errors='ignore'
        )
        return process.stdout.strip()
    except Exception:
        return None

def compare_outputs(actual, expected):
    """เปรียบเทียบผลลัพธ์ รองรับทั้งข้อความและทศนิยม"""
    if actual is None:
        return False
    actual_clean = actual.strip()
    expected_clean = expected.strip()
    
    if actual_clean.lower() == expected_clean.lower():
        return True
    
    try:
        return abs(float(actual_clean) - float(expected_clean)) < 1e-5
    except ValueError:
        return False

def main():
    total_score = 0
    max_total_score = 20
    summary_rows = []

    for exam_name, test_cases in EXAM_TEST_CASES.items():
        file_path = find_file(exam_name)
        passed_cases = 0
        total_cases = len(test_cases)
        
        if file_path:
            for inputs, expected in test_cases:
                output = run_test(file_path, inputs)
                if compare_outputs(output, expected):
                    passed_cases += 1
        
        # คะแนนยืดหยุ่น (1 เคส = 1 คะแนน)
        score_for_exam = passed_cases 
        total_score += score_for_exam
        
        if passed_cases == total_cases:
            status_icon = "✅ ผ่านครบ"
        elif passed_cases > 0:
            status_icon = "🟡 ผ่านบางส่วน"
        else:
            status_icon = "❌ ไม่ผ่าน"

        summary_rows.append(
            f"| `{exam_name}` | {status_icon} | {passed_cases}/{total_cases} เคส | **{score_for_exam} / 4** |"
        )

    markdown_summary = f"""# 📊 สรุปผลการสอบวิชาเขียนโปรแกรม (Set 6)

| ข้อสอบ | สถานะการตรวจ | ผ่าน Test Cases | คะแนนที่ได้ |
| :--- | :---: | :---: | :---: |
{chr(10).join(summary_rows)}

---

### 🎯 **คะแนนรวมทั้งหมด: {total_score} / {max_total_score} คะแนน**
"""

    print(markdown_summary)

    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_file:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_summary)

if __name__ == "__main__":
    main()
