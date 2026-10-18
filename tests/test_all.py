
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from langgraph.graph import END
from langgraph.types import Command

import graph.nodes as nodes


# --------------------------------------------------
# verification_node
# --------------------------------------------------

@patch("graph.nodes.engine")
def test_verification_node_customer_exists(mock_engine):
    connection = MagicMock()
    connection.execute.return_value.first.return_value = (1,)
    mock_engine.connect.return_value.__enter__.return_value = connection

    result = nodes.verification_node({"customer_id": "customer-123"})

    # Current implementation returns None for an existing customer.
    assert result is None
    connection.execute.assert_called_once()


@patch("graph.nodes.engine")
def test_verification_node_customer_does_not_exist(mock_engine):
    connection = MagicMock()
    connection.execute.return_value.first.return_value = None
    mock_engine.connect.return_value.__enter__.return_value = connection

    result = nodes.verification_node({"customer_id": "unknown-customer"})

    assert isinstance(result, Command)
    assert result.goto == END


# --------------------------------------------------
# node_1
# --------------------------------------------------

@patch("graph.nodes.llm")
def test_node_1_returns_selected_functions(mock_llm):
    mock_llm.with_structured_output.return_value.invoke.return_value = (
        SimpleNamespace(functions=["get_customer_orders"])
    )

    result = nodes.node_1({"customer_query": "Where is my order?"})

    assert result == {"node_1": ["get_customer_orders"]}
    mock_llm.with_structured_output.return_value.invoke.assert_called_once()


@patch("graph.nodes.llm")
def test_node_1_returns_empty_list_when_llm_fails(mock_llm):
    mock_llm.with_structured_output.return_value.invoke.side_effect = (
        Exception("LLM unavailable")
    )

    result = nodes.node_1({"customer_query": "Where is my order?"})

    assert result == {"node_1": []}


# --------------------------------------------------
# node_2
# --------------------------------------------------

@patch("graph.nodes.llm")
def test_node_2_returns_selected_functions(mock_llm):
    mock_llm.with_structured_output.return_value.invoke.return_value = (
        SimpleNamespace(functions=["get_customer_payments"])
    )

    result = nodes.node_2({"customer_query": "Did my payment go through?"})

    assert result == {"node_2": ["get_customer_payments"]}
    mock_llm.with_structured_output.return_value.invoke.assert_called_once()


@patch("graph.nodes.llm")
def test_node_2_returns_empty_list_when_llm_fails(mock_llm):
    mock_llm.with_structured_output.return_value.invoke.side_effect = (
        Exception("LLM unavailable")
    )

    result = nodes.node_2({"customer_query": "Check my payment"})

    assert result == {"node_2": []}


# --------------------------------------------------
# merge_list_node
# --------------------------------------------------

def test_merge_list_node_returns_empty_list_when_no_functions():
    state = {
        "customer_id": "customer-123",
        "customer_query": "Hello",
        "node_1": [],
        "node_2": [],
    }

    result = nodes.merge_list_node(state)

    assert result == {"blank_list": []}


@patch("graph.nodes.search_company_policy")
@patch("graph.nodes.get_customer_reviews")
@patch("graph.nodes.get_customer_payments")
@patch("graph.nodes.get_customer_sellers")
@patch("graph.nodes.get_customer_products")
@patch("graph.nodes.get_customer_order_items")
@patch("graph.nodes.get_customer_orders")
@patch("graph.nodes.get_customer_record")
def test_merge_list_node_calls_selected_functions(
    mock_record,
    mock_orders,
    mock_items,
    mock_products,
    mock_sellers,
    mock_payments,
    mock_reviews,
    mock_policy,
):
    mocks = {
        "get_customer_record": mock_record,
        "get_customer_orders": mock_orders,
        "get_customer_order_items": mock_items,
        "get_customer_products": mock_products,
        "get_customer_sellers": mock_sellers,
        "get_customer_payments": mock_payments,
        "get_customer_reviews": mock_reviews,
        "search_company_policy": mock_policy,
    }

    for function_name, mocked_function in mocks.items():
        mocked_function.return_value = {"function": function_name}

    state = {
        "customer_id": "customer-123",
        "customer_query": "Where is my order?",
        "node_1": ["get_customer_orders", "get_customer_record"],
        "node_2": ["get_customer_orders", "search_company_policy"],
    }

    result = nodes.merge_list_node(state)

    # Duplicate function names should be called only once.
    mock_orders.assert_called_once_with("customer-123")
    mock_record.assert_called_once_with("customer-123")
    mock_policy.assert_called_once_with("Where is my order?")

    assert len(result["blank_list"]) == 3
    assert {
        item["function"] for item in result["blank_list"]
    } == {
        "get_customer_orders",
        "get_customer_record",
        "search_company_policy",
    }


# --------------------------------------------------
# analyse_answer_node
# --------------------------------------------------

@patch("graph.nodes.llm")
def test_analyse_answer_node_when_no_information(mock_llm):
    mock_llm.invoke.return_value = SimpleNamespace(
        content="I don't have enough information to answer."
    )

    state = {
        "customer_query": "Hello",
        "blank_list": [],
    }

    result = nodes.analyse_answer_node(state)

    assert result == {
        "final_result": "I don't have enough information to answer."
    }
    mock_llm.invoke.assert_called_once()


@patch("graph.nodes.llm")
def test_analyse_answer_node_when_information_exists(mock_llm):
    mock_llm.invoke.return_value = SimpleNamespace(
        content="Your order is being processed."
    )

    state = {
        "customer_query": "What is my order status?",
        "blank_list": [{"order_status": "processing"}],
    }

    result = nodes.analyse_answer_node(state)

    assert result == {
        "final_result": "Your order is being processed."
    }
    mock_llm.invoke.assert_called_once()


@patch("graph.nodes.llm")
def test_analyse_answer_node_when_information_is_blank_string(mock_llm):
    mock_llm.invoke.return_value = SimpleNamespace(
        content="There isn't enough information."
    )

    state = {
        "customer_query": "Check my order",
        "blank_list": [""],
    }

    result = nodes.analyse_answer_node(state)

    assert result == {
        "final_result": "There isn't enough information."
    }
