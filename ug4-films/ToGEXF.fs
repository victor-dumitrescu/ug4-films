﻿module ToGEXF

open FSharp.Data
open ApiCalls
open Graph
open System

type OutputXml = XmlProvider<Sample="C:\Users\Victor\GitHub\ug4-films\ug4-films\hello-world.gexf.xml", InferTypesFromValues=false>

let id source target =
    sprintf "%s%s" source.id target.id

let constructXML (filmGraph: FilmGraph) =

    let nodes = OutputXml.Nodes [| for film in filmGraph do
                                     yield new OutputXml.Node(film.Key.id, film.Key.title)|]

    let edges = OutputXml.Edges [| for source in filmGraph do
                                       for target in source.Value do
                                            yield OutputXml.Edge((id source.Key target), source.Key.id, target.id)
                                            |]
    
    let graph = new OutputXml.Graph("static", "directed", nodes, edges)
    let meta = new OutputXml.Meta(DateTime.Now.Date.ToShortDateString(), "Victor Dumitrescu", "Rotten Tomatoes similarity graph")
    let gefx = new OutputXml.Gexf("1.2", meta, graph)

    //Bug in FSharp.Data? 
    //some elements are only detected if their name is capitalised
    (sprintf "%s \n %A" """<?xml version="1.0" encoding="UTF-8"?>""" gefx).Replace("Nodes>", "nodes>").Replace("Edges>", "edges>")
