#include <iostream>
#include <vector>
#include <cstring>
#include <fstream>
#include <iostream>
#include <string>
#include <stdlib.h>

using namespace std;
 struct node{
        string taxonomy;
        double percent_hit;
        int num_hits=0;

};

int main(int argc, char *argv[])
{
    char * genome_stats;
    char * taxonomy;

    if (argc==1){
        genome_stats = "v1S1_data_statistics_10e-3_coverage.txt";
        taxonomy="GBK_Taxonomy.txt";
    }
    else{
        taxonomy=argv[1]; // taxonomy NEEDS to be first command line arg
        genome_stats=argv[2];
    }
    ifstream oddish;
    double threshold = 5;
    char  junk [500];

    vector <node> viruses;

    oddish.open(taxonomy);
    if (!oddish.is_open()){cout<<"Unable to find taxonomy"<<endl; return 0;}
    while (oddish.peek()!=EOF){

        node temp;
        oddish.getline(junk, 500, '\n');
        temp.taxonomy = junk;
        viruses.push_back(temp); // create data structure of each virus from taxonomy generator
    }
    oddish.clear();
    oddish.close();
    oddish.open(genome_stats);
    if (!oddish.is_open()){cout<<"Unable to find statistics"<<endl; return 0;}

    oddish.getline(junk, 500, '\n'); // strip header

    char * virus_name;
    char * hits_to_genome;
    char * percent_proteins_hit;


    while(oddish.peek()!=EOF){
        oddish.getline(junk, 100, '\t');
        oddish.getline(junk, 100, '\t'); // get virus name
        virus_name=new char[strlen(junk)+1];
        sprintf(virus_name,"%s",junk);
        oddish.getline(junk, 100, '\t');
        oddish.getline(junk, 100, '\t'); // get hits to genome
        hits_to_genome=new char[strlen(junk)+1];
        sprintf(hits_to_genome,"%s",junk);
        oddish.getline(junk, 100, '\n'); // get percent proteins hit, end of line
        percent_proteins_hit=new char[strlen(junk)+1];
        sprintf(percent_proteins_hit,"%s",junk);

        for (int j = 0; j <viruses.size(); j++ ){ //search for current virus in taxonomy list
            string tax = viruses[j].taxonomy;
            size_t found = tax.find(virus_name);
            if (found!=std::string::npos){
                viruses[j].percent_hit = atoi(percent_proteins_hit);
                viruses[j].num_hits = atoi(hits_to_genome);
                break;
            }
        }
        delete virus_name;
        delete hits_to_genome;
        delete percent_proteins_hit;
    }


    oddish.clear();
    oddish.close();
    ofstream out;
    string output="TaxonomyXGenomeHits_";
    output+=genome_stats;

    char * m = (char *) output.c_str();
    out.open(m); // output file name unique to genome_stats file name

    for(int i = 0; i <viruses.size(); i++){
        if (viruses[i].num_hits!=0)
            out<<viruses[i].num_hits<<viruses[i].taxonomy<<endl;
    }
    out.clear();
    out.close();

    return 0;
}
