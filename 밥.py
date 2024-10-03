import tkinter as tk  # GUI 생성을 위한 tkinter 모듈
from tkinter import messagebox, ttk  # 메시지 박스와 ttk 모듈
import pandas as pd  # 데이터 처리를 위한 pandas 모듈

# 기본 영양 정보 엑셀 파일에서 불러오기
# 예시 데이터로 영양소 정보 데이터프레임 생성
nutrition_data = pd.DataFrame({
    '음식이름': ['바나나', '사과', '치킨'],
    '칼로리kcal': [89, 52, 239],
    '탄수화물': [22.8, 14, 0],
    '단백질': [1.1, 0.3, 27],
    '지방': [0.3, 0.2, 14],
    '비타민C': [8.7, 4.6, 0],
    '칼륨': [358, 107, 223],
    '철분': [0.3, 0.1, 1.3],
    '제아잔틴': [22, 29, 0],
    '비타민A': [64, 54, 15]
})
nutrition_data.set_index('음식이름', inplace=True)  # '음식이름'을 인덱스로 설정

# 사용자 영양 정보 초기화
# 사용자가 섭취한 영양소의 초기값을 0으로 설정
user_nutrition = {
    '칼로리kcal': 0, '탄수화물': 0, '단백질': 0, '지방': 0,
    '비타민C': 0, '칼륨': 0, '철분': 0, '제아잔틴': 0, '비타민A': 0
}

# 하루 권장량 설정
# 영양소 별로 하루 권장량을 설정한 딕셔너리
daily_recommendations = {
    '칼로리kcal': 2000, '탄수화물': 300, '단백질': 50, '지방': 70,
    '비타민C': 90, '칼륨': 3500, '철분': 18, '제아잔틴': 1000, '비타민A': 900
}

# 음식 추가 시 영양 정보를 업데이트하는 함수
def update_nutrition(food, grams):
    if food in nutrition_data.index:  # 입력한 음식이 데이터에 있는지 확인
        food_nutrition = nutrition_data.loc[food]  # 선택한 음식의 영양소 데이터를 가져옴
        for nutrient in user_nutrition:  # 각 영양소에 대해
            # 음식의 영양소 값을 섭취한 양에 따라 업데이트
            user_nutrition[nutrient] += (food_nutrition[nutrient] * grams / 100)
        update_display()  # 업데이트된 정보를 표시

# 영양 정보 표시를 업데이트하는 함수
def update_display():
    nutrition_text = ""  # 표시할 텍스트 초기화
    for nutrient, amount in user_nutrition.items():  # 각 영양소와 그 섭취량에 대해
        percent = (amount / daily_recommendations[nutrient]) * 100  # 권장량 대비 퍼센트 계산
        # 영양소와 퍼센트 값을 포맷하여 문자열로 만듦
        nutrition_text += f"{nutrient}: {amount:.2f}g ({percent:.2f}%)\n"
    # 텍스트 위젯을 활성화하고 업데이트된 정보를 표시한 후 비활성화
    nutrition_text_widget.config(state=tk.NORMAL)
    nutrition_text_widget.delete(1.0, tk.END)
    nutrition_text_widget.insert(tk.END, nutrition_text)
    nutrition_text_widget.config(state=tk.DISABLED)

# 음식 추가 버튼 클릭 시 호출되는 함수
def add_food():
    food = food_entry.get()  # 음식 입력란에서 값을 가져옴
    try:
        grams = float(grams_entry.get())  # 그램 입력란에서 값을 가져와 숫자로 변환
    except ValueError:  # 숫자가 아닌 값이 입력되면 에러 메시지 출력
        messagebox.showerror("입력 오류", "g 수치를 정확히 입력하세요.")
        return
    # 리스트박스에 음식과 그램 수 추가
    food_listbox.insert(tk.END, f"{food} {grams}g")
    update_nutrition(food, grams)  # 영양 정보 업데이트

# 음식 삭제 버튼 클릭 시 호출되는 함수
def delete_food():
    try:
        selected = food_listbox.curselection()[0]  # 선택한 항목의 인덱스를 가져옴
        food_listbox.delete(selected)  # 선택한 항목을 리스트박스에서 삭제
        messagebox.showinfo("삭제 완료", "선택한 음식을 삭제했습니다.")  # 삭제 완료 메시지
    except IndexError:  # 선택한 항목이 없으면 경고 메시지 출력
        messagebox.showwarning("선택 오류", "삭제할 음식을 선택하세요.")

# 수정 버튼 클릭 시 호출되는 함수
def modify_food():
    try:
        selected_index = food_listbox.curselection()[0]  # 선택한 항목의 인덱스를 가져옴
        selected_item = food_listbox.get(selected_index)  # 선택한 항목의 텍스트를 가져옴
        food_name = selected_item.split()[0]  # 음식 이름을 추출

        # 수정 내용을 적용하는 함수
        def apply_modification():
            try:
                new_grams = float(new_grams_entry.get())  # 새로운 그램 수 입력
            except ValueError:  # 잘못된 값이 입력되면 에러 메시지 출력
                messagebox.showerror("입력 오류", "g 수치를 정확히 입력하세요.")
                return
            # 리스트박스에서 기존 항목을 삭제하고 새로운 값을 추가
            food_listbox.delete(selected_index)
            food_listbox.insert(selected_index, f"{food_name} {new_grams}g")
            messagebox.showinfo("수정 완료", "음식 양이 수정되었습니다.")  # 수정 완료 메시지
            update_nutrition(food_name, new_grams)  # 영양 정보 업데이트
            modify_popup.destroy()  # 팝업 창 닫기

        # 수정 팝업 창 생성
        modify_popup = tk.Toplevel(window)
        modify_popup.title("수정")  # 팝업 창 제목 설정
        modify_popup.geometry("200x100")  # 팝업 창 크기 설정
        tk.Label(modify_popup, text="새로운 g 수치:").pack(pady=5)  # 입력 설명 라벨
        new_grams_entry = tk.Entry(modify_popup)  # 새로운 g 수치를 입력받는 Entry 위젯
        new_grams_entry.pack(pady=5)
        tk.Button(modify_popup, text="확인", command=apply_modification).pack(pady=5)  # 확인 버튼
    except IndexError:  # 선택한 항목이 없으면 경고 메시지 출력
        messagebox.showwarning("선택 오류", "수정할 음식을 선택하세요.")

# GUI 구성
window = tk.Tk()  # 메인 창 생성
window.title("음식 영양 성분 추적기")  # 창 제목 설정
window.geometry("600x400")  # 창 크기 설정

# 음식 입력란 생성
tk.Label(window, text="음식").grid(row=0, column=0)  # 음식 라벨
food_entry = tk.Entry(window)  # 음식 입력란
food_entry.grid(row=0, column=1)

tk.Label(window, text="g").grid(row=1, column=0)  # 그램 라벨
grams_entry = tk.Entry(window)  # 그램 입력란
grams_entry.grid(row=1, column=1)

# 추가, 삭제, 수정 버튼 생성
tk.Button(window, text="추가", command=add_food).grid(row=0, column=2)
tk.Button(window, text="삭제", command=delete_food).grid(row=1, column=2)
tk.Button(window, text="수정", command=modify_food).grid(row=2, column=2)

# 음식 리스트박스와 스크롤바 생성
food_listbox_frame = tk.Frame(window)  # 리스트박스와 스크롤바를 담을 프레임
food_listbox_frame.grid(row=0, column=3, rowspan=4, padx=10, pady=10)

food_listbox = tk.Listbox(food_listbox_frame, height=10)  # 음식 리스트박스 생성
food_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

food_scrollbar = tk.Scrollbar(food_listbox_frame)  # 리스트박스용 스크롤바 생성
food_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 리스트박스와 스크롤바를 연동
food_listbox.config(yscrollcommand=food_scrollbar.set)
food_scrollbar.config(command=food_listbox.yview)

# 영양 정보 표시 Text 위젯과 스크롤바 생성
nutrition_frame = tk.Frame(window)  # 영양 정보 표시용 프레임
nutrition_frame.grid(row=0, column=4, rowspan=4, padx=10, pady=10)

nutrition_text_widget = tk.Text(nutrition_frame, wrap=tk.WORD, height=10, width=30)  # 영양 정보 표시용 텍스트 위젯
nutrition_text_widget.pack(side=tk.LEFT, fill=tk.BOTH)
nutrition_text_widget.config(state=tk.DISABLED)  # 사용자가 수정하지 못하도록 비활성화

nutrition_scrollbar = tk.Scrollbar(nutrition_frame)  # 스크롤바 생성
nutrition_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 텍스트 위젯과 스크롤바를 연동
nutrition_text_widget.config(yscrollcommand=nutrition_scrollbar.set)
nutrition_scrollbar.config(command=nutrition_text_widget.yview)

window.mainloop()  # GUI 실행
