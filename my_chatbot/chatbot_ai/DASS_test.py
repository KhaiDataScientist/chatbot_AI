# Python program to administer the test based on the provided document

class DepressionTest:
    def __init__(self):
        # Questions and their options
        self.questions = {
            "Đề mục 1": "0: Tôi không cảm thấy buồn. \n 1: Nhiều lúc tôi cảm thấy chán hoặc buồn. \n 2: Lúc nào tôi cũng cảm thấy chán hoặc buồn và tôi không thể thôi được. \n3: Tôi rất buồn hoặc rất bất hạnh và khổ sở đến mức không thể chịu được.",
            "Đề mục 2": "0: Tôi hoàn toàn không bi quan và nản lòng về tương lai. \n1: Tôi cảm thấy nản lòng về tương lai hơn trước. \n2: Tôi cảm thấy mình chẳng có gì mong đợi ở tương lai cả. \n3: Tôi cảm thấy tương lai tuyệt vọng và tình hình chỉ có thể tiếp tục xấu đi hoặc không thể cải thiện được.",
            "Đề mục 3": "0: Tôi không cảm thấy như bị thất bại. \n 1: Tôi thấy mình thất bại nhiều hơn những người khác. \n2: Tôi cảm thấy đã hoàn thành rất ít điều đáng giá hoặc đã hoàn thành rất ít điều có ý nghĩa. \n3: Tôi cảm thấy mình là một người hoàn toàn thất bại.",
            "Đề mục 4": "0: Tôi hoàn toàn không bất mãn. \n1: Tôi ít thấy thích những điều mà tôi vẫn thường ưa thích trước đây. \n2: Tôi không thõa mãn về bất kỳ cái gì nữa. \n3: Tôi không còn chút thích thú nào nữa.",
            "Đề mục 5": "0: Tôi hoàn toàn không cảm thấy có tội lỗi gì ghê gớm cả. \n1: Phần nhiều những việc tôi đã làm tôi đều cảm thấy có tội. \n2: Tôi cảm thấy mình hoàn toàn có tội. \n3: Lúc nào tôi cũng cảm thấy mình có tội.",
            "Đề mục 6": "0: Tôi không cảm thấy đang bị trừng phạt. \n1: Tôi cảm thấy có thể mình sẽ bị trừng phạt. \n2: Tôi mong chờ bị trừng phạt. \n3: Tôi cảm thấy mình đang bị trừng phạt.",
            "Đề mục 7": "0: Tôi thấy bản thân mình vẫn như trước kia. \n1: Tôi thất vọng với bản thân. \n2: Tôi ghê tởm bản thân. \n3: Tôi ghét bản thân mình.",
            "Đề mục 8": "0: Tôi không phê phán hoặc đổ lỗi cho bản thân. \n1: Tôi phê phán bản thân mình nhiều hơn trước kia. \n2: Tôi phê phán bản thân về tất cả những lỗi lầm của mình. \n3: Tôi đổ lỗi cho bản thân về tất cả mọi điều tồi tệ xảy ra.",
            "Đề mục 9": "0: Tôi không có ý nghĩ tự sát. \n1: Tôi có ý nghĩ tự sát nhưng không thực hiện. \n2: Tôi muốn tự sát. \n3: Nếu có cơ hội tôi sẽ tự sát.",
            "Đề mục 10": "0: Tôi không khóc nhiều hơn trước kia. \n1: Hiện nay tôi hay khóc nhiều hơn trước. \n2: Tôi thường khóc vì những điều nhỏ nhặt. \n3: Tôi thấy muốn khóc nhưng không thể khóc được.",
            "Đề mục 11": "0: Tôi không dễ bồn chồn và căng thẳng hơn thường lệ. \n1: Tôi cảm thấy dễ bồn chồn và căng thẳng hơn thường lệ. \n2: Tôi cảm thấy bồn chồn và căng thẳng đến mức khó có thể ngồi yên được. \n3: Tôi thấy rất bồn chồn và kích động đến mức phải đi lại liên tục hoặc làm việc gì đó."
            # ... Continue with the remaining questions
        }
        self.total_scores = 0
    def administer_test(self):
        print("Trả lời các câu hỏi dựa trên cảm nhận của bạn trong tuần vừa qua.")
    
        for question,answer in self.questions.items():
            print(f"Câu {question}:\n{answer}")
            is_number = False
            while not is_number:
                try:
                    score = int(input("Điểm của bạn cho câu này (0-3): "))
                    if score>=0 and score<4:
                        is_number = True
                        self.total_scores += score
                except ValueError as e:
                    print( 'Nhập lại đúng số đi bạn')


        return self.total_scores

    def interpret_score(self):
        if self.total_scores < 14:
            return "Không biểu hiện trầm cảm"
        elif 14 <= self.total_scores <= 19:
            return "Trầm cảm nhẹ"
        elif 20 <= self.total_scores <= 29:
            return "Trầm cảm vừa"
        else:
            return "Trầm cảm nặng"


# Example of using the class
test = DepressionTest()
scores = test.administer_test()
result = test.interpret_score()

