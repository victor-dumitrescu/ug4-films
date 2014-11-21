module ToGEXF

open FSharp.Data
open Graph
open System

type OutputXml = XmlProvider<Sample="..\data\char-graph.gexf.xml", InferTypesFromValues=false>

let mutable edgeID = 0
let nextEdgeID() =
    edgeID <- edgeID + 1
    sprintf "%d" edgeID

let constructXML (graph: CharGraph) =
    
    let nodes = OutputXml.Nodes [| for character in graph.Keys do
                                      yield OutputXml.Node(character, character) |]

    let edges = OutputXml.Edges [| for dict in graph do
                                      for character in dict.Value do
                                            yield OutputXml.Edge(nextEdgeID(), dict.Key, character.Key, character.Value.ToString()) |]

    let graph = OutputXml.Graph("static", "undirected", nodes, edges)
    let meta = OutputXml.Meta(DateTime.Now.Date.ToShortDateString(), "Victor Dumitrescu", "Character graph")
    let gefx = OutputXml.Gexf("1.2", meta, graph)

    (sprintf "%s \n %A" """<?xml version="1.0" encoding="UTF-8"?>""" gefx).Replace("Nodes>", "nodes>").Replace("Edges>", "edges>")