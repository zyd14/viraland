#include <iostream>
#include "string.h"
#include <vector>
#include <cstring>
#include <fstream>
#include <stdlib.h>

using namespace std;
// must pass in all_files.txt FIRST then GKB_taxonomy.txt
int main(int argc, char *argv[])
{
    //char *path="C:\\Users\\Jon\\Documents\\School\\Code Prjcts\\TaxonomyFromGBK\\AllPhageGBK\\";
    //int num_files=1470;
    if (argc !=1){cout<<"Invalid number of arguments"<<endl; return 0;}
    char * all_files = argv[1];
    char *file_name=new char [500];
    char *junk=new char [500];
    ifstream in;
    ofstream out;
    out.open("GBK_taxonomy.txt");

    vector <char *> file_names;


    in.open(all_files);
    if (in.is_open()){
        while(in.peek()!=EOF)
            {
                in.getline(junk,500,'\n');
                file_names.push_back(junk);
                junk="";

               // cout << acc[i] << " " <<i<<endl;
            }
        in.clear();
        in.close();
    }

    int jj = 1;
    for (int j = 0; j < file_names.size(); j++){


        in.open(file_names[j]);
        if(!in.is_open()) {cout << "cant find file " << jj<< "" << file_name << endl; jj++; continue;}
        //else {cout<< file_name<<" good"<<endl;}

        in.getline(junk, 500, '\n');

        string token = "ORGANISM";
        bool next_file = false;
        while (in.peek()!=EOF && next_file==false){
            in.getline(junk, 500, '\n');
            string z = junk;
            size_t found = z.find(token);
            if (found!=std::string::npos){
                    string temp;
                    vector <string> fields;
                    int pos = found+token.length()+1;
                    temp = z.substr(pos, z.length()-1); // get first field, organism species
                    fields.push_back(temp);
                    temp = "";
                    in.getline(junk, 500, '\n');
                    z=junk;
                    int counter = 0;
                    while (z[counter]==' ') // strip junk spaces
                        counter ++;
                    for (int j = counter; j<z.length(); j++){
                        if (z[j]!=';' && z[j]!='.')
                            temp+=z[j];
                        else {fields.push_back(temp); temp="";}

                    }
                    out<<fields[0]<<"\t";
                    for (int i =fields.size()-1; i>1; i--){
                        out<<fields[i]<<"\t";
                    }
                    out<<fields[1]<<endl;
                    fields.clear();
                    found = std::string::npos;
                    next_file = true;
                    in.close();
                    in.clear();


            }
        }
    } out.clear(); out.close();
}
