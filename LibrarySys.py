from tkinter import *
import sqlite3
from sqlite3 import Error
import datetime

def createConnection(db_file):           
    try:                                        #create a connection with the database file
        global db
        db = sqlite3.connect(db_file)
        
        createTables()                          #create the tables
        
    except Error as e:                          #exceptions for any errors that might come up
        print(e)

        
    readTables()                                #read the data from the database
    


def  createTables():                #creating the tables
    cursor = db.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")      
    cursor.execute('CREATE TABLE members(id INTEGER PRIMARY KEY, name TEXT, itemsBorrowed INTEGER , maxItems INTEGER)')     #creating the members table
    cursor.execute('CREATE TABLE items(id INTEGER PRIMARY KEY, title TEXT, author text , status text)')                     #creating the items table
    cursor.execute("""CREATE TABLE loan(   
    id INTEGER PRIMARY KEY,
    memberId INTEGER,
    itemId INTEGER,
    issuesDate TEXT,
    returnDate TEXT,
    FOREIGN KEY(memberId) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY(itemId) REFERENCES items(id) ON DELETE CASCADE)""")                                                         #creating the loan table


def readTables():                       #a subroutine that runs all the subroutines that read tables
    readMembersTable()
    readItemsTable()
    readLoanTable()
    db.commit()
    
def readMembersTable():                 #a subroutine that stores the content of the member table in a list
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    for row in rows:
        i = Member(row[0], row[1], row[2],row[3])
        members.append(i)
      
    

def readItemsTable():                   #a subroutine that stores the content of the item table in a list
    cursor = db.cursor()
    cursor.execute("SELECT * FROM items")
                   
    rows = cursor.fetchall()
    for row in rows:
        i = Item(row[0], row[1], row[2],row[3])
        
        items.append(i)
        
    

def readLoanTable():                #a subroutine that stores the content of the loan table in a list
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM loan")
    rows = cursor.fetchall()
    global loans
    loans = []
    for row in rows:
        i = Loan(row[0], row[1], row[2],row[3] , row[4])
        
        loans.append(i)
    



class Item:                                                                 #Item class
    def __init__(self, itemId, title, author, status = "Available"):         #initialising the class
        self.itemId = itemId
        self.title = title
        self.author = author
        self.status= status

    def display(self):                                                      #function to display an item
        item = formating(self.itemId, 10) + formating(self.title, 20) + formating(self.author, 25) + formating(self.status, 15)
        return item

        
class Member:                                                           #Memeber class
    def __init__(self, memberId,name,itemsBorrowed,maxItems = 5):       #initialising the class
        self.memberId = memberId
        self.name = name
        self.itemsBorrowed = itemsBorrowed
        self.maxItems = maxItems

    def display(self):                                                   #function to display a member
            item = formating(self.memberId, 10) + formating(self.name, 20) + formating(self.itemsBorrowed, 25) + formating(self.maxItems, 15)
            return item




class Loan:                                                                         #Loan class
    def __init__(self, loanId, memberId, itemId, issueDate, returnDate ):     #initialising the class
        self.loanId = loanId
        self.memberId = memberId
        self.itemId = itemId
        self.issueDate = issueDate
        
        if returnDate:
            self.returnDate = returnDate
        else:
            self.returnDate = "NR"
    

    def display(self):                          # a function that returns infromation about the loab as a string
        loanText =  formating(self.loanId, 10) + formating(self.memberId, 15) + formating(self.itemId, 10) + formating(self.issueDate, 15) + formating(self.returnDate, 15)
        return loanText



    def confirmLoanReturn(self):                #confirming the loan 
        if self.returnDate == "NR":
            self.returnDate = datetime.date.today().strftime('%d/%m/%y')        #if the return date isn't already assigned then set it to the current date








def accessItems():                          #a subroutine that is called when the access items button is pressed
    mainFrame.pack_forget()                 #hides the mainframe and shows the item frame   
    itemFrame.pack()

def accessMembers():
    mainFrame.pack_forget()                 #hides the mainframe and shows the item frame   
    memberFrame.pack()

def accessLoans():
    mainFrame.pack_forget()                 #hides the mainframe and shows the item frame   
    loanFrame.pack()
    pass


def itemCreate():               #a subroutine that is called when the create button is pressed
 
    itemFrame.pack_forget()     #hide the current frame and show the item create frame
    createItemFrame.pack()
    
    


    
def itemDelete():               #a subroutine that is called when the delete button is pressed
   
    if LBXitems.curselection():                 # if an item is selected then deleted the item and update the listbox
        index = LBXitems.curselection()[0]
        itemId = items[index].itemId
        del items[index]
        cursor = db.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (itemId,))         #deleting the item from the database
    updateItems()

def returnMainFrame():                          #when the return button is pressed the current frame gets hiden and the main frame is shown
    mainFrame.pack()
    itemFrame.pack_forget()
    
def displayingItem(i,title,author, status):             #a function that gets the inputs of an item and dispays it in the desired format
    item = formating(i, 10) + formating(title, 20) + formating(author, 25) + formating(status, 15)
    return item
    
def formating(item, length):                           # a function that takes one item and return it with the proper length
    text = str(item)
    text = text + " " * (length-len(text))
    return text


def updateItems():                          # a subroutine that updates the items in the listbox
    LBXitems.delete(0,'end')
    for item in items:                      # a loop that goes through all the items list and inserts them in the listbox
        LBXitems.insert(END, item.display())
        
    if items:
        ID = int(items[len(items) -1].itemId) +1     #getting the ID of the next item
    else:
        ID = 1
    EBXid.configure(state=NORMAL)               #enabling the ID entrybox
    EBXid.delete(0, 'end')                      #deleting it's content
    EBXid.insert(0, ID)                         # inserting the ID variable into the entrybox
    EBXid.configure(state='readonly')           #reverting the entrybox to read only
    db.commit()


def cancel():                               #a function that is called when the cancel button is pressed and it hides the current frame and shows the item frame
    createItemFrame.pack_forget()
    itemFrame.pack()

def save():                                 # a function that is called when the save button is pressed
    createItemFrame.pack_forget()           #hide the current frame and show the item frame
    itemFrame.pack()
    
    savedItem = Item(EBXid.get(),EBXtitle.get(),EBXauthor.get(),EBXstatus.get())  # retrieve the data from the entryboxes
    items.append(savedItem)                                                                 #add the saved item to the items list and update the listbox
    cursor = db.cursor()
    cursor.execute('INSERT INTO items(title, author, status) VALUES(?,?,?)', (savedItem.title, savedItem.author, savedItem.status)) #adding the item to the database
    db.commit()
    updateItems()                                                                       
    
    EBXtitle.delete(0, 'end')
    EBXauthor.delete(0, 'end')              #delete the content of the entryboxes
    EBXstatus.delete(0, 'end')

def itemSearch():                           #subroutine that updates the listbox depending on the query
    if EBXtitleQuery.get() or EBXauthorQuery.get():     #if either of the entryboxes are not empty then run the code
        cursor = db.cursor()                            
        cursor.execute("SELECT * FROM items WHERE title like ?  and author like ?",("%" + EBXtitleQuery.get() + "%", "%" + EBXauthorQuery.get() + "%"))     #a query that retrieves an item depending on the title and author
        
        rows = cursor.fetchall()                    
        itemsTemp=[]                    #creating a temporary list to store the query into
        global items
        for row in rows:
            i = Item(row[0], row[1], row[2],row[3])
            itemsTemp.append(i)
            items = itemsTemp.copy()                        #copying the content of the temporary list into the items one
        
        updateItems()                                       

def itemClear():                        #a subroutine that clears the query result and the content of the entryboxes
    EBXtitleQuery.delete(0,END)
    EBXauthorQuery.delete(0,END)
    global items
    items = []
    readItemsTable()
    updateItems()
    


def createMember():               #a subroutine that is called when the create button is pressed
    
    memberFrame.pack_forget()       #hides the current frame and shows the memeber create frame
    createMemeberFrame.pack()
    
    
    
   
def deleteMember():               #a subroutine that is called when the delete button is pressed
    
    if LBXmembers.curselection():                 # if a member is selected then deleted the memeber from the member list and update the listbox
        index = LBXmembers.curselection()[0]
        memberId = members[index].memberId
        del members[index]
        cursor = db.cursor()
        cursor.execute('DELETE FROM members WHERE id = ?', (memberId,))     #deleting the member from the database

    updateMember()
    
def returnMember():              #when the return button is pressed the current frame gets hiden and the main frame is shown
    
    mainFrame.pack()
    memberFrame.pack_forget()


    
def displayingMember(i,title,author, status):             #a function that gets the inputs of an item and dispays it in the desired format
    item = formating(i, 10) + formating(title, 20) + formating(author, 25) + formating(status, 15)
    return item



def updateMember():                                     # a subroutine that updates the listbox for the memebers
    LBXmembers.delete(0,'end')                          # clear the listbox
    for member in members:                                # a loop that adds the memeber to the listbox
        LBXmembers.insert(END, member.display())
    if members:
        ID = int(members[len(members) -1].memberId) +1           # get the ID and incremented by 1
    else:
        ID = 1
    EBXmemberID.configure(state=NORMAL)                 # set the state of the memeberID entrybox to normal so it is possible to edit the text
    EBXmemberID.delete(0, 'end')                        #delete the content of the entrybox
    EBXmemberID.insert(0, ID)                           #insert the ID in the entrybox
    EBXmemberID.configure(state='readonly')             #set the entrybox to readonly
    db.commit()

def cancelMember():             # a subrouitne that is called when the cancel button is pressed and it hides the current frame and shows the memeber frame
    
    createMemeberFrame.pack_forget()
    memberFrame.pack()

def saveMember():               # a subroutine that is called when the save button is pressed                              

    createMemeberFrame.pack_forget()        #hide the current frame and show the member frame
    memberFrame.pack()
    
    savedItem = Member(EBXmemberID.get(),EBXmemberName.get(),EBXmemberBorrowed.get(),EBXmemberMax.get())  #retrieve the data for the entry boxes
    
    members.append(savedItem)               #add that data to the member list and update the listbox
    

    cursor = db.cursor()

    cursor.execute('INSERT INTO members(name, itemsBorrowed, maxItems) VALUES(?,?,?)', (savedItem.name, savedItem.itemsBorrowed, savedItem.maxItems)) #adding the member into the database
    db.commit()
    updateMember()
    
    EBXmemberName.delete(0, 'end')
    EBXmemberBorrowed.delete(0, 'end')      #delete the content of the listboxes
    EBXmemberMax.delete(0, 'end')



def displayingloan(i,memberId,itemId, issueDate, returnDate):             #a function that gets the inputs of an item and dispays it in the desired format
    item = formating(i, 10) + formating(memberId, 15) + formating(itemId, 10) + formating(issueDate, 15) + formating(returnDate, 15)
    return item
    
def createLoan():                                                   #a subroutine that hides the current frame and shows the loan frame
    loanCreateFrame.pack()
    loanFrame.pack_forget()
    
def updateLoan():                                                   #a subroutine that updates the loan listbox
    LBXloans.delete(0,'end')
    readLoanTable()
    for item in loans:
        LBXloans.insert(END, item.display())
    if loans:    
        ID = int(loans[len(loans) -1].loanId) +1        #getting the ID of the next loan
    else:
        ID = 1
    EBXloanID.configure(state=NORMAL)               #enabling the ID entrybox
    EBXloanID.delete(0, 'end')                      #deleting it's content
    EBXloanID.insert(0, ID)                         #inserting the ID variable into the entrybox
    EBXloanID.configure(state='readonly')           #reverting the entrybox to read only
    db.commit()
    
    
def confirmReturn():                            #confirm that the selected loan has been returned by changing the return date to the current day
   
    if LBXloans.curselection():                 
        index = LBXloans.curselection()[0]
        loans[index].confirmLoanReturn()
        cursor = db.cursor()
        cursor.execute("UPDATE loan SET returnDate = ? WHERE id = ? ", (loans[index].returnDate, loans[index].loanId))
        readLoanTable()
        updateLoan()
        

def loanSave():                             #a subroutine that is called when the save button is pressed
    loanFrame.pack()
    loanCreateFrame.pack_forget()           #hides the current frame and shows the loan fram
    
    savedLoan = Loan(EBXloanID.get(), EBXloanMemberID.get() , EBXloanItemID.get(), datetime.date.today().strftime('%d/%m/%y') , "")  #get the data from the entryboxes and add it to the loan list
    loans.append(savedLoan)

    cursor = db.cursor()
    cursor.execute('INSERT INTO loan(memberId, itemId, issuesDate) VALUES(?,?,?)', (savedLoan.memberId, savedLoan.itemId, savedLoan.issueDate)) #Save the loan to the database    

    db.commit()
    updateLoan()

    EBXloanMemberID.delete(0,'end')
    EBXloanItemID.delete(0,'end')
    

def loanCancel():                   #a subrotuine that is called when the cancel button is pressed
    loanFrame.pack()
    loanCreateFrame.pack_forget()   #hides the current frame and shows the loan fram

def loanRetrun():                   #a subrotuine that is called when the return button is called and it hides the current frame and shows the main frame
    loanFrame.pack_forget()
    mainFrame.pack()


    
root = Tk()                     #initialising the window and giving a title
root.title("Library")           #setting the title of the window
root.resizable(False, False)    #Making the window non resizable

items = []  #a list of items
members = []  #a list of members
loans = []  #a list of loans



mainFrame = Frame(root)         #the main frame that is shown at first
mainFrame.pack()                





BTNAcessItems = Button(mainFrame, text = "Access Items", width =20, command = accessItems , font = "TkFixedFont").grid(row=0,column=0,sticky=W) #items button that hides the current frame and shows the item frame

BTNAcessMemebers = Button(mainFrame, text = "Access Memebers", width =20, command = accessMembers , font = "TkFixedFont").grid(row=1,column=0,sticky=W)#memeber button that hides the current frame and shows the member frame

BTNAcessLoans = Button(mainFrame, text = "Access Loans", width =20, command = accessLoans , font = "TkFixedFont").grid(row=2,column=0,sticky=W)#loan button that hides the current frame and shows the loan frame


itemFrame = Frame(root)         #creating a frame that the item selection will go in


LBLcategories = Label(itemFrame, text = displayingItem("ID" , "Titles","Authors", "Status"), font = "TkFixedFont") # creating the label that will display the categories of the propreties of the item
LBLcategories.grid(row=0,column = 0,columnspan = 4 , sticky=W)

LBXitems = Listbox(itemFrame, width = 75 , font = "TkFixedFont" )    #creating a listbox that will hold the items
LBXitems.grid(row=1,column = 0,sticky=W  ,rowspan=3, columnspan = 4)

BTNitemCreate = Button(itemFrame, text="Create Item", width = 15, command=itemCreate,  font = "TkFixedFont").grid(row=1,column=4,sticky=W)  #button that hides the current frame and shows the createitem frame
BTNitemDelete = Button(itemFrame, text="Delete Item", width = 15, command=itemDelete,  font = "TkFixedFont").grid(row=2,column=4,sticky=W)  #button deletes the current selection
BTNreturn = Button(itemFrame, text="Return", width = 15, command=returnMainFrame,  font = "TkFixedFont").grid(row=3,column=4,sticky=W)      #button that hides the current frame and shows the main frame



LBLtitleQuery = Label(itemFrame,text = "Title", width=15, font="TkFixedFont") .grid(row=4,column=0,sticky=W)    # labels to show what the query entryboxes are
LBLauthorQuery = Label(itemFrame,text = "Author", width=15, font="TkFixedFont") .grid(row=4,column=2,sticky=W)

EBXtitleQuery = Entry(itemFrame,width=15, font="TkFixedFont")
EBXtitleQuery .grid(row=4,column=1,sticky=W)                        
                                                                                #entryboxes for the queries
EBXauthorQuery = Entry(itemFrame,width=15, font="TkFixedFont")
EBXauthorQuery.grid(row=4,column=3,sticky=W)


BTNitemSearch = Button(itemFrame, text="Search", width = 15, command=itemSearch,  font = "TkFixedFont").grid(row=5,column=0,sticky=N, columnspan = 2)   #search button that runs the query

BTNitemclear = Button(itemFrame, text="Clear ", width = 15, command=itemClear,  font = "TkFixedFont").grid(row=5,column=2,sticky=N, columnspan =2 )     #clear button that clears the result of the query and the entryboxes



createItemFrame = Frame(root)   #creating a frame that allows for the creation of items

LBLid  = Label(createItemFrame, text = formating("ID", 10), font = "TkFixedFont" ).grid(row=0,column = 0 , sticky=W)    

LBLtitles  = Label(createItemFrame, text = formating("Titles", 20), font = "TkFixedFont").grid(row=0,column = 1 , sticky=W)

LBLauthor  = Label(createItemFrame, text = formating("Author", 25), font = "TkFixedFont").grid(row=0,column = 2 , sticky=W)             #labels that show what the entryboxes do

LBLstatus  = Label(createItemFrame, text = formating("Status", 15), font = "TkFixedFont").grid(row=0,column = 3 , sticky=W)



EBXid = Entry(createItemFrame, width = 8,font = "TkFixedFont" )
EBXid.grid(row=1,column=0,sticky=W)

EBXtitle = Entry(createItemFrame , width = 18,font = "TkFixedFont")
EBXtitle.grid(row=1,column=1,sticky=W)

EBXauthor = Entry(createItemFrame , width = 23,font = "TkFixedFont")                    #Entryboxes so the user can enter data about the item
EBXauthor.grid(row=1,column=2,sticky=W)

EBXstatus = Entry(createItemFrame , width = 13,font = "TkFixedFont")
EBXstatus.grid(row=1,column=3,sticky=W)



BTNSave = Button(createItemFrame, text = "Save", width =15, command = save , font = "TkFixedFont").grid(row=2,column=1,sticky=W)    #button that takes the data from the texboxes and saves it

BTNCancel = Button(createItemFrame, text = "Cancel", width =15, command = cancel , font = "TkFixedFont").grid(row=2,column=2,sticky=W)  #button that hides the current frame and shows the item frame









memberFrame = Frame(root)         #creating a frame that the member selection will go in

LBLmemberCategories = Label(memberFrame, text = displayingMember("ID" , "Name","Item Borrowed", "Max Items"), font = "TkFixedFont") # creating the label that will display the categories of the propreties of the memebers
LBLmemberCategories.grid(row=0,column = 0,columnspan = 4 , sticky=W)

LBXmembers = Listbox(memberFrame, width = 75 , font = "TkFixedFont" )    #creating a listbox that will hold the members
LBXmembers.grid(row=1,column = 0,sticky=W  ,rowspan=3, columnspan = 4)

BTNcreate = Button(memberFrame, text="Create Member", width = 15, command=createMember,  font = "TkFixedFont").grid(row=1,column=4,sticky=W)  #hides current frame and shows the create member frame
BTNdelete = Button(memberFrame, text="Delete Member", width = 15, command=deleteMember,  font = "TkFixedFont").grid(row=2,column=4,sticky=W)  #deletes the current selection
BTNreturn = Button(memberFrame, text="Return", width = 15, command=returnMember,  font = "TkFixedFont").grid(row=3,column=4,sticky=W)       #hides current frame and shows the main frame


createMemeberFrame = Frame(root)            #creating a frame that the member will be created in

LBLmemberID  = Label(createMemeberFrame, text = formating("ID", 10), font = "TkFixedFont" ).grid(row=0,column = 0 , sticky=W)               

LBLmemberName  = Label(createMemeberFrame, text = formating("Name", 20), font = "TkFixedFont").grid(row=0,column = 1 , sticky=W)                #labels that shows what each entrybox represents

LBLmemberBorrowed  = Label(createMemeberFrame, text = formating("Item Borrowed", 25), font = "TkFixedFont").grid(row=0,column = 2 , sticky=W)

LBLmemberMax = Label(createMemeberFrame, text = formating("Max Items", 15), font = "TkFixedFont").grid(row=0,column = 3 , sticky=W)

EBXmemberID = Entry(createMemeberFrame, width = 8,font = "TkFixedFont" )            
EBXmemberID.grid(row=1,column=0,sticky=W)

EBXmemberName = Entry(createMemeberFrame , width = 18,font = "TkFixedFont")                     #entryboxes so the user can input the data about members    
EBXmemberName.grid(row=1,column=1,sticky=W)

EBXmemberBorrowed = Entry(createMemeberFrame , width = 23,font = "TkFixedFont")
EBXmemberBorrowed.grid(row=1,column=2,sticky=W)

EBXmemberMax = Entry(createMemeberFrame , width = 13,font = "TkFixedFont")
EBXmemberMax.grid(row=1,column=3,sticky=W)


BTNSave = Button(createMemeberFrame, text = "Save", width =15, command = saveMember , font = "TkFixedFont").grid(row=2,column=1,sticky=W)   #retrieves the textbox input and saves it then hides the current frame and shows the memeber frame

BTNCancel = Button(createMemeberFrame, text = "Cancel", width =15, command = cancelMember , font = "TkFixedFont").grid(row=2,column=2,sticky=W) #hides the current frame and shows the memeber frame





loanFrame = Frame(root)     # a frame used to display the loans



LBLcategories = Label(loanFrame, text = displayingloan("ID" , "Memeber ID","Item ID", "Loan Date" , "Return Date"), font = "TkFixedFont") # creating the label that will display the categories of the propreties of the item
LBLcategories.grid(row=0,column = 0,columnspan = 4 , sticky=W)

LBXloans = Listbox(loanFrame, width = 65 , font = "TkFixedFont" )    #creating a listbox that will hold the items
LBXloans.grid(row=1,column = 0,sticky=W  ,rowspan=3, columnspan = 4)


BTNloanCreate= Button(loanFrame, text="Create Loan", width = 15, command=createLoan,  font = "TkFixedFont").grid(row=1,column=4,sticky=W)           #create button that hides the current frame and shows the create loan frame
BTNloanConfirm = Button(loanFrame, text="Confirm return", width = 15, command=confirmReturn,  font = "TkFixedFont").grid(row=2,column=4,sticky=W)   #confirm return button that changes the return date to the current date
BTNloanReturn = Button(loanFrame, text="Return", width = 15, command = loanRetrun,  font = "TkFixedFont").grid(row=3,column=4,sticky=W)             #return button that hides the current frame and shows the main frame

loanCreateFrame = Frame(root)       #a frame used to create loans

LBLloanID = Label(loanCreateFrame, text = formating("LoanID", 15), font = "TkFixedFont").grid(row=0,column = 0 , sticky=W)
LBLloanMemberID = Label(loanCreateFrame, text = formating("Member ID", 15), font = "TkFixedFont").grid(row=0,column = 1 , sticky=W)         #labels to show what the entryboxes are used for
LBLloanItemID = Label(loanCreateFrame, text = formating("Item ID", 15), font = "TkFixedFont").grid(row=0,column = 2 , sticky=W)


EBXloanID = Entry(loanCreateFrame, width = 8,font = "TkFixedFont" )            
EBXloanID.grid(row=1,column=0,sticky=W)

EBXloanMemberID = Entry(loanCreateFrame, width = 8,font = "TkFixedFont" )                           #entryboxes so the user can enter data about the loans
EBXloanMemberID.grid(row=1,column=1,sticky=W)

EBXloanItemID = Entry(loanCreateFrame, width = 8,font = "TkFixedFont" )            
EBXloanItemID.grid(row=1,column=2,sticky=W)

BTNloanSave = Button(loanCreateFrame, text="Save", width = 10, command=loanSave,  font = "TkFixedFont").grid(row=2,column=0,sticky=N, columnspan = 2)           #save button used to retrieve the data from the entryboxes aswell as hide the current frame and show the loan frame
BTNLoanCancel = Button(loanCreateFrame, text="Cancel", command=loanCancel, width = 10,   font = "TkFixedFont").grid(row=2,column=1,sticky=N, columnspan = 2)    #cancel button hides the current frame and shows the loan frame











createConnection("LibaryDatabase.db") #Inititalising a connection with the database file if it does exist and if it doesn't then it gets created

updateItems()                   #update the item listbox so it shows the cocntent of the items list

updateMember()                  #update the memeber listbox so it shows the content of the memebers list

updateLoan()                    #update the loan listbox so it shows the loans

root.mainloop()                 #the mainloop that keeps the tkinter window open
