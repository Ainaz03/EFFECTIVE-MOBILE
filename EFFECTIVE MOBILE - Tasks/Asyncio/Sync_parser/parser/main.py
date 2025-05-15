import logging
from Sync_parser.parser.extractor import find_new_excel_link_from_all_pages, extract_filename
from Sync_parser.parser.file_manager import download_file_from_url
from Sync_parser.parser.file_processor import process_file
from Sync_parser.parser.database_tools import save_processedfile_to_db
from Sync_parser.sync_database import Session

def find_and_process_new_file():
    session = Session()
    try:        
        new_file_url = find_new_excel_link_from_all_pages(session)

        if new_file_url:
            file_name = extract_filename(new_file_url)
            if download_file_from_url(new_file_url) and process_file(session, file_name):
                save_processedfile_to_db(session, new_file_url, file_name)
                logging.info(f"Файл {file_name} успешно обработан.\n")
                return True
        return False

    except Exception as e:
        session.rollback()
        logging.error(f"[Ошибка] {e}")
        return False
    
    finally:
        session.close()