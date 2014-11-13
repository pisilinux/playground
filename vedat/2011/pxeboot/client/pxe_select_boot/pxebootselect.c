#include  <stdio.h>
#include  <stdlib.h>
#include  <string.h>
#include  <malloc.h>
#include <locale.h>

#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

#include <ncurses.h>
#include <curses.h>
#include <menu.h>

#define ROW    20 
#define COL    70
#define ROW_MIN    17
#define COL_MIN    53
#define MENU_SIZE   14


typedef struct vers {
    char *versionID;
    char *name;
    char *size;
    char *path;
} vers, *versPtr;

typedef struct gversion {
    int nbversions;
    versPtr versions[500]; /* using dynamic alloc is left as an exercise */
} gVersion, *gVersPtr;

FILE *fp;
char *machtype;

void getMachType(void)
{
    FILE *fP;
    
    if ((fP = popen("uname -m", "r")) == NULL) { 
        printf("Machtype not found\n" );
        return;
    }

    if ((machtype = (char *)calloc(20, 0)) == NULL) {
        printf("Cannot allocate memory...\n");
        return;
    }
    fread(machtype, sizeof(machtype), 1, fP);
    
    if (strrchr(machtype, '\n'))
        *strrchr(machtype, '\n') = '\0';
    
    fclose(fP);
}

//-----   PARSE XML   -----//
static versPtr parseVersion(xmlDocPtr doc, xmlNodePtr cur) {
    versPtr ret = NULL;

    ret = (versPtr) malloc(sizeof(vers));
    if (ret == NULL) {
        fprintf(stderr,"out of memory\n");
    return(NULL);
    }
    memset(ret, 0, sizeof(vers));

    /* We don't care what the top level element name is */
    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Name")) )
            ret->name = (char *)xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Path")) )
            ret->path = (char *)xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Size")) )
            ret->size = (char *)xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Architecture")) )
            ret->versionID = (char *)xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
        cur = cur->next;
    }

    return(ret);
}


//------------------------------------------------------------------------------------------------------

static gVersPtr parseGversFile(char *filename) {
    xmlDocPtr doc;
    gVersPtr ret;
    versPtr curvers;
    xmlNodePtr cur;

#ifdef LIBXML_SAX1_ENABLED

    doc = xmlParseFile(filename);
    if (doc == NULL) return(NULL);
#else
    return(NULL);
#endif /* LIBXML_SAX1_ENABLED */

    cur = xmlDocGetRootElement(doc);

    ret = (gVersPtr) malloc(sizeof(gVersion));
    if (ret == NULL) {
        fprintf(stderr,"out of memory\n");
        xmlFreeDoc(doc);
        return(NULL);
    }
    memset(ret, 0, sizeof(gVersion));
    cur = cur->xmlChildrenNode;
    while ( cur && xmlIsBlankNode ( cur ) ) {
        cur = cur -> next;
    }
    if ( cur == 0 ) {
        xmlFreeDoc(doc);
        free(ret);
        return ( NULL );
    }

    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
        if ((!xmlStrcmp(cur->name , (const xmlChar *) "Pardus")))  {
            curvers = parseVersion(doc , cur);
            if (curvers != NULL)
               if (strstr(curvers->name, machtype))
                    ret->versions[ret->nbversions++] = curvers;
            if (ret->nbversions >= 500)
                break;
        }
        cur = cur->next;
    }

    return(ret);
}


//============================================================================================================

void print_in_middle(WINDOW *win, int starty, int startx, int width,
    char *string, chtype color)
{
    int length, x, y;
    float temp;

    if(win == NULL)
        win = stdscr;
    getyx( win , y , x );
    if(startx != 0)
        x = startx;
    if(starty != 0)
        y = starty;
    if(width == 0)
        width = 80;

    length = strlen(string);
    temp = (width - length)/ 2;
    x = startx + (int)temp;
    wattron(win , color);
    mvwprintw(win , y , x , "%s", string);
    wattroff(win , color);
    refresh();

}
//-------------------------------------------------------------------------------


void screen_size(WINDOW *win, int min_row, int min_col,int *r, int *c)
{
    int row,col;
    getmaxyx(win,row,col);
    if ((row<min_row) || (col<min_col))
     {
         endwin();
         printf("\n\nScreen's too small..bitch!\n1-resize the screen\n2-restart the program.\n\n\n");
         exit(EXIT_SUCCESS);
     }

     *r = row;
     *c = col;
}

//-------------------------------------------------------------------------------

int main(int argc, char **argv)
{
    setlocale(LC_ALL , "");

    int i;
    gVersPtr cur;
    char programname[50];
    /* COMPAT: Do not genrate nodes for formatting spaces */
    LIBXML_TEST_VERSION

    xmlKeepBlanksDefault(0);
    
    getMachType();
    
    cur = parseGversFile(argv[1]);
    /* Clean up everything else before quitting. */
    xmlCleanupParser();
    
    ITEM **my_items;
    MENU *my_menu;
    WINDOW *my_menu_win;
    int n_choices = 0;

    n_choices = cur->nbversions; 
    my_items = (ITEM **)calloc(n_choices + 1, sizeof(ITEM *));
    for (i = 0; i < cur->nbversions; i++)
        my_items[i] = new_item(cur->versions[i]->name, cur->versions[i]->versionID);
    
    sprintf(programname, "Pardus PXE-Boot - %s", machtype);
    
    /* Curses kipini ilklendir*/
    initscr();
    int row,col;
    screen_size(stdscr,ROW_MIN,COL_MIN,&row,&col);

    start_color();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    init_pair(1, COLOR_RED, COLOR_BLACK);
    init_pair(2, COLOR_CYAN, COLOR_BLACK);
    init_pair(3, COLOR_MAGENTA, COLOR_BLACK);
    
    /* Menüyü oluştur */
    my_menu = new_menu((ITEM **)my_items);
    
    /* Menü ile ilişiklendirilecek pencereyi oluştur */
    my_menu_win = newwin( ROW , COL , row / 2 - ROW/2, col / 2 - COL/2);
    keypad(my_menu_win, TRUE);
    
    /* Ana pencereyi ve alt pencereleri ayarla */
    set_menu_win(my_menu, my_menu_win);
    set_menu_sub(my_menu, derwin(my_menu_win , ROW-4 , COL-2 , 4 , 2 ));
    set_menu_format(my_menu , MENU_SIZE , 1);  //tek bi sayfa için gösterilmesini istediğimiz satır sayısı


    /* Menü göstericisini " * " olarak ayarla*/
    set_menu_mark(my_menu, " >> ");

    /* Ana pencere etrafında bir çerçeve çiz ve bir başlık yaz */
    box(my_menu_win, 0, 0);
    print_in_middle( my_menu_win, 1 , 0 , COL , programname , COLOR_PAIR(1) );
    mvwaddch(my_menu_win , 2 , 0 , ACS_LTEE);
    mvwhline(my_menu_win , 2 , 1 , ACS_HLINE, COL-2);
    
    attron( COLOR_PAIR(3) );
    mvprintw( LINES - 3 , 0 , "ABCDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ" );
    mvprintw( LINES - 2 , 0 , "F1 to exit\n,  abcdefgğhıijklmeoöprsştuüvyz" );
    attroff( COLOR_PAIR(3) );
    refresh();

    /* Menüyü ekrana yaz */
    post_menu( my_menu );
    wrefresh( my_menu_win );

    char path[256];
    int len=0, limit=0;
    int c = 0;
    
    do
    {
        c = wgetch(my_menu_win);
        switch(c)
        {
            case KEY_DOWN:
                if(limit < n_choices - 1){
                    limit++;
                    len= strlen(cur->versions[limit]->name)+strlen(cur->versions[limit]->versionID)+ strlen(cur->versions[limit]->size)+2*4;
                    attron( COLOR_PAIR(2) );
                    menu_driver( my_menu , REQ_DOWN_ITEM );
                    move(60, 0);
                    clrtoeol();
                    mvprintw( LINES-10 , 0 , "\n");
                    mvprintw( LINES-10 , col/2 - len/2 , "%s    %s    %s",
                    item_name( current_item( my_menu )) , cur->versions[limit]->versionID , cur->versions[limit]->size );
                    pos_menu_cursor( my_menu );
                    attroff( COLOR_PAIR(2) );
                }
                break;
            case KEY_UP:
                 if( limit > 0 ){
                    limit--;
                    len= strlen( cur->versions[limit]->name ) + strlen( cur->versions[limit]->versionID )+ strlen( cur->versions[limit]->size ) + 2*4;
                    attron( COLOR_PAIR(2) );
                    menu_driver( my_menu , REQ_UP_ITEM);
                    move(60, 0);
                    clrtoeol();
                    mvprintw( LINES-10 , 0 , "\n");
                    mvprintw( LINES-10 , col/2 - len/2 , "%s    %s    %s",
                    item_name( current_item(my_menu)) ,cur->versions[limit]->versionID , cur->versions[limit]->size );
                    pos_menu_cursor( my_menu );
                    attroff( COLOR_PAIR(2) );
                 }
                break;
            case 10: /* Enter */
                 strcpy(path,"PXEISOFILE=");
                 strcat( path , cur->versions[limit]->path);
                 fp = fopen("/etc/pxeisofile","w");
                 if (!fp)
                 {
                     printf("it failed!\n");
                 }
                 else
                 {
                     fputs(path , fp);
                     fclose(fp);
                    mvprintw( LINES-7 , 0 , "STARTING BOOT ");
                 }
                 c = KEY_F(1);
                 break;
            default:
                 break;
        
        } 
        refresh();
    } while (c != KEY_F(1));

     

    /* Menüyü ekrandan sil ve tahsis edilen belleği geri ver */
     unpost_menu(my_menu);
     for(i = 0; i < n_choices; ++i)
         free_item(my_items[i]);
     free(machtype);
     free_menu(my_menu);
     endwin();

 return 0;
}
