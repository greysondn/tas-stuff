#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// WSL - i686-w64-mingw32-g++ -static-libgcc -static-libstdc++ -o name.exe name.cpp
#include <windows.h>

// I'm being lazy, fix your own code.
using namespace std;

// load dictionary, nothing fancy
vector<string> loadDictionary()
{
    // eventual return
    vector<string> ret;
    
    // load dictionary
    string nextWord = "";
    ifstream dictFile("dict.txt");
    
    // inject into vector
    if (dictFile.is_open())
    {
        while (getline(dictFile, nextWord))
        {
            ret.push_back(nextWord);
        }
        
        dictFile.close();
    }
    else
    {
        cout << "Something went wrong loading dictionary!" << endl;
        cin.get();
    }
    
    // end
    return ret;
}

void loadBoard(string (&ret)[12])
{
    // load board
    string nextLine = "";
    ifstream boardFile("board.txt");
    
    // inject into array
    if (boardFile.is_open())
    {
        string onlyLine = "";
        
        getline(boardFile, onlyLine);
        
        for (int i=0; i < 12; i++)
        {
            for (int j=(i*14); j < ((i * 14) + 14); j++)
            {
                nextLine = nextLine + onlyLine[j];
            }
            
            // set to entry in array
            ret[i] = nextLine;
            
            // clear line for next to come in
            nextLine = "";
        }
        
        boardFile.close();
    }
    else
    {
        cout << "Something went wrong loading board!" << endl;
        cin.get();
    }
}

bool compareString(string onBoard, string dictWord)
{
    bool ret = true;
    
    for (int i = 0; i < dictWord.length(); i++)
    {
        if (i > onBoard.length())
        {
            ret = false;
        }
        else if (dictWord[i] != onBoard[i])
        {
            ret = false;
        }
    }
    
    return ret;
}

void checkForWord(string onBoard, string dictWord, string direction, int xCoord, int yCoord)
{
    if (compareString(onBoard, dictWord))
    {
        cout << endl;
        cout << "FOUND! --> " << dictWord << endl;
        cout << "X: " << xCoord << endl;
        cout << "Y: " << yCoord << endl;
        cout << "DIRECTION: " << direction << endl;
        cout << endl;
    }
}

void checkEntireDictionary(vector<string> dict, string onBoard, string direction, int xCoord, int yCoord)
{
    for (unsigned i=0; i < dict.size(); i++)
    {
        checkForWord(onBoard, dict[i], direction, xCoord, yCoord);
    }
}

void checkUp(vector<string> dict, string board[12], int xCoord, int yCoord)
{
    // up
    string boardLine = "";
    
    // to go down, y decreases
    for (int y = yCoord; y >= 0; y--)
    {
            boardLine = boardLine + board[y][xCoord];
    }
    
    // and then just check that againt an entire dictionary
    checkEntireDictionary(dict, boardLine, "up", xCoord, yCoord);
}

int main()
{
    // load dictionary
    vector<string> dict = loadDictionary();
    
    // print dictionary
    // for (unsigned i=0; i < dict.size(); i++)
    // {
    //     cout << dict[i] << endl;
    // }
    
    // load board
    string board[12];
    
    for (int i = 0; i < 12; i++)
    {
        board[i] = "";
    }
    
    loadBoard(board);
    
    for (int i=0; i < 12; i++)
    {
        cout << board[i] << endl;
    }
    
    // must be time to search that board, eh?
    
    // sytematically, cell by cell, please
    for (int x = 0; x < 14; x++)
    {
        for (int y = 0; y < 12; y++)
        {
            // some of these at least have helper functions now.
            checkUp(dict, board, x, y);
            
            // up right is a little harder
            string boardUpRight = "";
            int upRight_x = x;
            int upRight_y = y;
            bool upRight_done = false;
            
            while (!upRight_done)
            {
                boardUpRight = boardUpRight + board[upRight_y][upRight_x];
                
                // progress iteration
                upRight_x = upRight_x + 1;
                upRight_y = upRight_y - 1;
                
                if ((upRight_x >= 14) || (upRight_y < 0))
                {
                    upRight_done = true;
                }
            }
            
            checkEntireDictionary(dict, boardUpRight, "up-right", x, y);
            
            // right
            string boardRight = "";
            
            for (int bx = x; bx < 14; bx++)
            {
                boardRight = boardRight + board[y][bx];
            }
            
            checkEntireDictionary(dict, boardRight, "right", x, y);
            
            // down right
            string boardDownRight = "";
            int downRight_x = x;
            int downRight_y = y;
            bool downRight_done = false;
            
            while (!downRight_done)
            {
                boardDownRight = boardDownRight + board[downRight_y][downRight_x];
                
                // progress iteration
                downRight_x = downRight_x + 1;
                downRight_y = downRight_y + 1;
                
                if ((downRight_x >= 14) || (downRight_y >= 12))
                {
                    downRight_done = true;
                }
            }
            
            checkEntireDictionary(dict, boardDownRight, "down-right", x, y);
            
            // down
            string boardDown = "";
            
            for (int by = y; by < 12; by++)
            {
                boardDown = boardDown + board[by][x];
            }
            
            checkEntireDictionary(dict, boardDown, "down", x, y);
            
            // down left
            string boardDownLeft = "";
            int downLeft_x = x;
            int downLeft_y = y;
            bool downLeft_done = false;
            
            while (!downLeft_done)
            {
                boardDownLeft = boardDownLeft + board[downLeft_y][downLeft_x];
                
                // progress iteration
                downLeft_x = downLeft_x - 1;
                downLeft_y = downLeft_y + 1;
                
                if ((downLeft_x < 0) || (downLeft_y >= 12))
                {
                    downLeft_done = true;
                }
            }
            
            checkEntireDictionary(dict, boardDownLeft, "down-left", x, y);
            
            // left
            string boardLeft = "";
            
            for (int bx = x; bx >= 0; bx--)
            {
                boardLeft = boardLeft + board[y][bx];
            }
            
            checkEntireDictionary(dict, boardLeft, "left", x, y);
            
            // up-left
            string boardUpLeft = "";
            int upLeft_x = x;
            int upLeft_y = y;
            bool upLeft_done = false;
            
            while (!upLeft_done)
            {
                boardUpLeft = boardUpLeft + board[upLeft_y][upLeft_x];
                
                // progress iteration
                upLeft_x = upLeft_x - 1;
                upLeft_y = upLeft_y - 1;
                
                if ((upLeft_x < 0) || (upLeft_y < 0))
                {
                    upLeft_done = true;
                }
            }
            
            checkEntireDictionary(dict, boardUpLeft, "up-left", x, y);
        }
    }
    
    // return
    return 0;
}