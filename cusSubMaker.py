class SubMaker:
    def __init__(self):
        self.subs = []

    def create_sub(self, time_range, text):
        # time_range là tuple (offset, duration) với đơn vị hiện tại có thể là micro giây
        start, duration = time_range
        
        # Chuyển đổi micro giây sang mili giây
        start_ms = start // 1000
        duration_ms = duration // 1000
        
        # Giới hạn duration tối đa để tránh kéo dài
        duration_ms = min(duration_ms, 2000)  # Giới hạn tối đa 2 giây nếu cần

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
