

from toevent_pagemove_youtube import content_youtube as cy
from insert_recode_in_mongo import connect_mongo as cm

def main():

    ip_add = f'mongodb://192.168.0.63:27017/'
    db_name = f'youtube_db_sanghoonlee'
    col_name = f'youtube_col_sanghoonlee'

    content_lists = cy.run_content_from_youtube()

    cm.insert_recode_in_mongo(ip_add, db_name, col_name, content_lists)

    pass


if __name__ == '__main__':
    main()
    pass