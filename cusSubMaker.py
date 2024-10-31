class SubMaker:
    def __init__(self):
        self.subs = []

    def create_sub(self, time_range, text):
        # time_range là tuple (offset, duration) với đơn vị là micro * 10
        start, duration = time_range
        
        # Chuyển đổi giá trị từ micro * 10 sang mili giây
        start_ms = start // 10000  # Chia cho 10 để chuyển sang micro giây
        duration_ms = duration // 10000  # Tương tự cho duration

        # Giới hạn duration tối đa nếu cần
        duration_ms = min(duration_ms, 2000)  # Giới hạn tối đa 2 giây
        
        end_ms = start_ms + duration_ms
        self.subs.append((start_ms, end_ms, text))

    def generate_subs(self):
        vtt_content = "WEBVTT\n\n"
        
        for start, end, text in self.subs:
            start_time = self.format_time(start)
            end_time = self.format_time(end)
            vtt_content += f"{start_time} --> {end_time}\n{text}\n\n"
        
        return vtt_content

    @staticmethod
    def format_time(milliseconds):
        hours = milliseconds // 3600000
        minutes = (milliseconds % 3600000) // 60000
        seconds = (milliseconds % 60000) // 1000
        millis = milliseconds % 1000
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(millis):03}"
